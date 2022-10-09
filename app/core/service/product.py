
from app.core.repository.product import ProductRepository


class ProductService:

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def create(self, data):
        return self._repository.create(data)

    def update(self, pk, data):
        return self._repository.update(pk, data)

    def get_all(self):
        return self._repository.get_all()

    def get_by_id(self, id):
        return self._repository.get_by_id(id)
