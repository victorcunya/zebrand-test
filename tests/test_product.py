
from app.interface.rest.main import app


def test_create_product_without_permissions(client, add_product):
    body = {
        "sku": "12345678",
        "name": "Laptop HP I5 - 16GB RAM",
        "brand": "HP",
        "price": 3150
    }

    with app.container.product_repo.override(add_product):
        response = client.post("api/products", json=body)

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated"

