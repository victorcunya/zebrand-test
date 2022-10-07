
from abc import ABCMeta, abstractmethod

from app.core.schema.product import ProductBase


class ProductRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, data: ProductBase):
        raise NotImplementedError
