
from app.core.containers import Container
from app.core.schema import product, tracking, user
from app.interface.rest import create_app
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = create_app()
app.container = Container()
product_service = app.container.product()
user_service = app.container.user()
tracking_service = app.container.tracking()

router = APIRouter()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Could not validate credentials', 
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        user = await user_service.get_current_user(token)
        if user is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return user


@router.post("/products", tags=["Product"])
def create_product(
    body: product.ProductBase,
    user: user.User = Depends(get_current_user),
):
    if user.role != 'ADMIN_ROLE':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    product = product_service.create(body)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Product sku {body.sku} already exists."
        )
    return product

@router.put("/products/{product_id}", tags=["Product"])
def update_product(
    product_id: int,
    body: product.ProductUpdate,
    user: user.User = Depends(get_current_user)
):
    if user.role != 'ADMIN_ROLE':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    product = product_service.get_by_id(product_id)
    if not product or not product.state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product disabled"
        )
    return product_service.update(product_id, body)

@router.delete("/products/{product_id}", tags=["Product"])
def delete_product(
    product_id: int,
    user: user.User = Depends(get_current_user)
):
    if user.role != 'ADMIN_ROLE':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    product = product_service.delete(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return {"deleted": True}

@router.get("/products", tags=["Product"])
def get_products(
    user: user.User = Depends(get_current_user)
):
    if user.role != 'ADMIN_ROLE':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return product_service.get_all()

@router.get("/products/{product_id}", tags=["Product"])
def get_product_by_id(
    product_id: int,
    user: user.User = Depends(get_current_user)
):
    product = product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with id {product_id} not found"
        )
    if not product.state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product.name} disabled"
        )
    if user.role == 'USER_ROLE':
        data = tracking.TrackingBase(entity= "Product", data_id=product_id)
        tracking_service.create(data)
    return product

@router.post("/token", tags=["Auth"], response_model=user.Token)
def create_access_token(data: user.TokenData):
    user = user_service.authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user_service.create_access_token(data)

@router.post("/users", tags=["User"], response_model=user.User)
def create_user(
    data: user.UserCreate,
    user: user.User = Depends(get_current_user)
):
    if user.role != 'ADMIN_ROLE':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = user_service.create(data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"email {data.email} already exists."
        )
    return user

@router.put("/users/{user_id}", tags=["User"], response_model=user.User)
def update_user(
    user_id: int,
    data: user.UserUpdate,
    user: user.User = Depends(get_current_user)
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Can't update, belongs to user {user.email} - ID:{user.id}"
        )
    return user_service.update(user_id, data)

@router.delete("/users/{user_id}", tags=["User"])
def delete_user(
    user_id: int, 
    user: user.User = Depends(get_current_user)
):
    if user.role != 'ADMIN_ROLE':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_service.delete(user_id)
    return {"deleted": True}


app.include_router(router, prefix="/api")
