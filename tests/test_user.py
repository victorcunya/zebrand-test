
from app.interface.rest.main import app


def test_create_access_token(client, add_user_admin):
    body = {
        "email": "admin@admin.com",
        "password": "admin"
    }
    with app.container.user_repo.override(add_user_admin):
        response = client.post("api/token", json=body)
    
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] is not None
    assert data['token_type'] == "bearer"

