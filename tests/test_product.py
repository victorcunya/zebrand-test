
from unittest import mock

from app.core.repository.mail import MailRepository
from app.core.repository.product import ProductRepository
from app.core.service.product import ProductService
from app.interface.rest.main import app


def test_create_product_without_permissions(client, add_product):
    body = {
        "sku": "12345678",
        "name": "Laptop HP I5 - 16GB RAM",
        "brand": "HP",
        "price": 3150
    }

    with app.container.product_repository.override(add_product):
        response = client.post("api/products", json=body)

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated"


def test_create_product(product):

    product_repo_mock = mock.Mock(spec=ProductRepository)
    product_repo_mock.create.return_value = product

    mail_repo_mock = mock.Mock(spec=MailRepository)
    mail_repo_mock.send_mail.return_value = []

    service = ProductService(
        product_repository=product_repo_mock,
        mail_repository=mail_repo_mock
    )

    body = {
        "sku": "12345678",
        "name": "Laptop HP I5 - 16GB RAM",
        "brand": "HP",
        "price": 3150
    }
    response = service.create(body)

    assert body["sku"] == response.sku
    assert body["name"] == response.name
    assert body["brand"] == response.brand
    assert body["price"] == response.price


def test_get_product_by_id(product):
    product_repo_mock = mock.Mock(spec=ProductRepository)
    product_repo_mock.get_by_id.return_value = product

    mail_repo_mock = mock.Mock(spec=MailRepository)
    mail_repo_mock.send_mail.return_value = []

    service = ProductService(
        product_repository=product_repo_mock,
        mail_repository=mail_repo_mock
    )

    response = service.get_by_id(product.id)

    assert product.id == response.id
    assert product.sku == response.sku
    assert product.name == response.name
    assert product.brand == response.brand
    assert product.price == response.price


def test_get_all_products(products):
    product_repo_mock = mock.Mock(spec=ProductRepository)
    product_repo_mock.get_all.return_value = products

    mail_repo_mock = mock.Mock(spec=MailRepository)
    mail_repo_mock.send_mail.return_value = []

    service = ProductService(
        product_repository=product_repo_mock,
        mail_repository=mail_repo_mock
    )

    response = service.get_all()

    assert response == products
