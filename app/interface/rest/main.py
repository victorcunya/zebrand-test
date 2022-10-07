
from app.core.containers import Container
from app.core.schema import product
from app.interface.rest import create_app
from fastapi import APIRouter

app = create_app()
app.container = Container()

router = APIRouter()

@router.get(
    "/hello"
)
def hello():
    return "Hello world!"

@router.post(
    "/products",
    tags=["Product"]
)
def create_product(body: product.ProductBase):
    product_service = app.container.product()
    return product_service.create(body)

app.include_router(router, prefix="/api")
