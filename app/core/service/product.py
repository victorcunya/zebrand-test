
from app.core.repository.product import ProductRepository


class ProductService:

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def create(self, data):
        return self._repository.create(data)
