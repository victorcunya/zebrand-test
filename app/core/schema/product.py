
from pydantic import BaseModel


class ProductBase(BaseModel):
    sku: str
    name: str
    price: float
    brand: str


class Product(ProductBase):
    id: int
    state: int
    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    price: float
    brand: str
