

from contextlib import AbstractAsyncContextManager
from typing import Callable

from app.core.repository.product import ProductRepository
from sqlalchemy.orm import Session

from .models import Product


class ProductDB(ProductRepository):

    def __init__(self, session: Callable[..., AbstractAsyncContextManager[Session]]) -> None:
        self._session_factory = session

    def create(self, data):
        with self._session_factory() as session:
            product = Product(
                sku=data.sku,
                name=data.name,
                price=data.price,
                brand=data.brand,
            )
            session.add(product)
            session.commit()
            session.refresh(product)
            return product

