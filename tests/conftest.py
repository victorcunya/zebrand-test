
from unittest import mock

import pytest
from app.core.schema.product import Product
from app.core.schema.user import User
from app.infrastructure.adapters.postgres.product import ProductDB
from app.infrastructure.adapters.postgres.user import UserDB
from app.interface.rest.main import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture
def product():
    product = Product(
        id=1,
        sku='12345678', 
        name='Laptop HP I5 - 16GB RAM', 
        price=3150,
        brand='HP',
        state=1
    )
    return product

@pytest.fixture
def add_product(product):
    product_repo_mock = mock.Mock(spec=ProductDB)
    product_repo_mock.create.return_value = product
    return product_repo_mock


@pytest.fixture
def user_admin():
    user = User(
        id=1,
        name='admin',
        email='admin@admin.com',
        password='$2b$12$ynjZtzZe4UzG5gQkPmD0cuf3AZxitdRw5Ko1ZZow2/CYYIH9ZiF7a',
        role='ADMIN_ROLE',
        state=1
    )
    return user

@pytest.fixture
def user_anonymous():
    user = User(
        id=2,
        name='user',
        email='user@admin.com',
        password='$2b$12$mvfcIU6Hu3VQqrOYQ.ucNeebJNNF7bDdKAOdcLL9jUlhyKjoGkfD6',
        role='USER_ROLE',
        state=1
    )
    return user


@pytest.fixture
def add_user_admin(user_admin):
    user_repo_mock = mock.Mock(spec=UserDB)
    user_repo_mock.create.return_value = user_admin
    user_repo_mock.get_user_by.return_value = user_admin
    return user_repo_mock


@pytest.fixture
def add_user_anonymous(user_anonymous):
    user_repo_mock = mock.Mock(spec=UserDB)
    user_repo_mock.create.return_value = user_anonymous
    user_repo_mock.get_user_by.return_value = user_anonymous
    return user_repo_mock


@pytest.fixture
def token(client, user_admin):
    body = {
        "email": "admin@admin.com",
        "password": "admin"
    }
    with app.container.user_repo.override(user_admin):
        response = client.post("api/token", json=body)
    
    data = response.json()
    return data['access_token']
