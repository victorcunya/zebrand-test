
from app.interface.rest.main import app


def test_create_access_token(client, get_user):
    body = {
        "email": "admin@admin.com",
        "password": "admin"
    }
    with app.container.user_repo.override(get_user):
        response = client.post("api/token", json=body)
    
    assert response.status_code == 200
    print(response)

