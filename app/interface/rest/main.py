
from app.core.containers import Container
from app.core.schema import product, user
from app.interface.rest import create_app
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = create_app()
app.container = Container()

router = APIRouter()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Could not validate credentials', 
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        user_service = app.container.user()
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
    product_service = app.container.product()
    return product_service.create(body)

@router.put("/products/{product_id}", tags=["Product"])
def update_product(
    product_id: int,
    body: product.ProductUpdate
):
    product_service = app.container.product()
    return product_service.update(product_id, body)

@router.delete("/products/{product_id}", tags=["Product"])
def delete_product(product_id: int):
    product_service = app.container.product()
    return {"delte": product_id}

@router.get("/products", tags=["Product"])
def get_products():
    product_service = app.container.product()
    return product_service.get_all()

@router.get("/products/{product_id}", tags=["Product"])
def get_product_by_id(product_id: int):
    product_service = app.container.product()
    return product_service.get_by_id(product_id)

@router.post("/token", tags=["Auth"], response_model=user.Token)
def create_access_token(data: user.TokenData):
    user_service = app.container.user()
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
def create_user(data: user.UserCreate):
    user_service = app.container.user()
    return user_service.create(data)



app.include_router(router, prefix="/api")
