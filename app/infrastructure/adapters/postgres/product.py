

from contextlib import AbstractAsyncContextManager
from typing import Callable

from app.core.repository.product import ProductRepository
from app.core.schema.product import Product
from sqlalchemy.orm import Session

from .models import Product as ProductModel


class ProductDB(ProductRepository):

    def __init__(self, session: Callable[..., AbstractAsyncContextManager[Session]]) -> None:
        self._session_factory = session

    def create(self, data):
        with self._session_factory() as session:
            product = ProductModel(
                sku=data.sku,
                name=data.name,
                price=data.price,
                brand=data.brand,
            )
            session.add(product)
            session.commit()
            session.refresh(product)
            return product

    def update(self, pk, data):
        with self._session_factory() as session:
            product = session.query(
                ProductModel.id,
                ProductModel.name,
                ProductModel.sku,
                ProductModel.brand,
                ProductModel.price,
            ).get(pk).\
                update(**data.dict())
            session.add(product)
            session.commit()
            session.refresh(product)
            return product

    def get_all(self):
        list_products = []
        with self._session_factory() as session:
            products = session.query(
                ProductModel.id,
                ProductModel.name,
                ProductModel.sku,
                ProductModel.brand,
                ProductModel.price,
            ).all()
            for item in products:
                list_products.append(Product.from_orm(item))
        return list_products

    def get_by_id(self, pk):
        product = None
        with self._session_factory() as session:
            data = session.query(
                ProductModel.id,
                ProductModel.name,
                ProductModel.sku,
                ProductModel.brand,
                ProductModel.price,
            ).get(pk)
            if data:
                product = Product.from_orm(data)
        return product
