
from abc import ABCMeta, abstractmethod

from app.core.schema.product import ProductBase, ProductUpdate


class ProductRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, data: ProductBase):
        raise NotImplementedError

    @abstractmethod
    def update(self, pk:int, data: ProductUpdate):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pk: int):
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk: int):
        raise NotImplementedError
