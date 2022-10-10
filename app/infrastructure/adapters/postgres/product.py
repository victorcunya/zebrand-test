

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
            return Product.from_orm(product)

    def update(self, pk, data):
        with self._session_factory() as session:
            product = session.query(ProductModel).get(pk).\
                update(**data.dict())
            session.add(product)
            session.commit()
            session.refresh(product)
            return Product.from_orm(product)

    def get_all(self):
        list_products = []
        with self._session_factory() as session:
            products = session.query(
                ProductModel.id,
                ProductModel.name,
                ProductModel.sku,
                ProductModel.brand,
                ProductModel.price,
                ProductModel.state
            ).filter_by(state=1)
            for item in products:
                list_products.append(Product.from_orm(item))
        return list_products

    def get_by_id(self, pk):
        try:
            with self._session_factory() as session:
                data = session.query(
                    ProductModel.id,
                    ProductModel.name,
                    ProductModel.sku,
                    ProductModel.brand,
                    ProductModel.price,
                    ProductModel.state,
                ).filter_by(id=pk).one()
            return Product.from_orm(data)
        except Exception:
            return None

    def delete(self, pk):
        try:
            with self._session_factory() as session:
                product = session.query(ProductModel).get(pk).\
                    update(**{"state": 0})
                session.add(product)
                session.commit()
                session.refresh(product)
                return product
        except Exception:
            None
