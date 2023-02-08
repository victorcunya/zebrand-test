
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from app.core.repository.mail import MailRepository
from app.core.repository.product import ProductRepository
from app.core.repository.user import UserRepository
from app.core.schema.product import Product
from app.core.schema.user import User
from app.infrastructure.adapters.postgres import Base, Database
from app.interface.rest.main import app

# Create the new database session
SQLALCHEMY_DATABASE_URL = 'postgresql://local:local@zebrand_db/test'


@pytest.fixture(scope="session")
def session():
    db = Database(SQLALCHEMY_DATABASE_URL)
    Base.metadata.drop_all(bind=db._engine)
    Base.metadata.create_all(bind=db._engine)

    yield db


@pytest.fixture()
def client():

    db = Database(SQLALCHEMY_DATABASE_URL)
    Base.metadata.drop_all(bind=db._engine)
    Base.metadata.create_all(bind=db._engine)
    
    app.container.db.reset()
    app.container.db.override(db)

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
def products(product):
    array_products = [product]
    array_products.append(
        Product(
            id=2,
            sku='87654321',
            name='Go Pro',
            price=1599,
            brand='Go',
            state=1
        )
    )
    return array_products


@pytest.fixture
def add_product(product):
    product_repo_mock = mock.Mock(spec=ProductRepository)
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
    user_repo_mock = mock.Mock(spec=UserRepository)
    user_repo_mock.create.return_value = user_admin
    user_repo_mock.get_user_by.return_value = user_admin
    return user_repo_mock


@pytest.fixture
def add_user_anonymous(user_anonymous):
    user_repo_mock = mock.Mock(spec=UserRepository)
    user_repo_mock.create.return_value = user_anonymous
    user_repo_mock.get_user_by.return_value = user_anonymous
    return user_repo_mock


@pytest.fixture
def token(client, add_user_admin):
    body = {
        "email": "admin@admin.com",
        "password": "admin"
    }
    with app.container.user_repository.override(add_user_admin):
        response = client.post("api/token", json=body)
    
    data = response.json()
    return data['access_token']
