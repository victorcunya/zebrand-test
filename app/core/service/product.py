
from app.core.repository.mail import MailRepository
from app.core.repository.product import ProductRepository
from app.core.schema.mail import MailBase
from app.core.schema.product import ProductUpdate


class ProductService:

    def __init__(self, 
        repository: ProductRepository, 
        mail_repository: MailRepository
    ):
        self._repository = repository
        self._mail_repository = mail_repository

    def create(self, data):
        return self._repository.create(data)

    def update(self, id, data: ProductUpdate):
        product = self._repository.update(id, data)
        if product:
            mail = MailBase(
                subject=f'Updated Product #{id}', 
                body=str(data.dict())
            )
            self._mail_repository.send_mail(mail)
        return product

    def get_all(self):
        return self._repository.get_all()

    def get_by_id(self, id):
        return self._repository.get_by_id(id)

    def delete(self, id):
        product = self._repository.delete(id)
        if product:
            mail = MailBase(
                subject=f'Deleted Product #{id}', 
                body=f'Product {product.name} - sku: {product.sku}, deleted!'
            )
            self._mail_repository.send_mail(mail)
        return product
