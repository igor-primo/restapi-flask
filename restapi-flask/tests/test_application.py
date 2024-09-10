import pytest
from application import create_app


class TestApplication:

    @pytest.fixture
    def client(self):
        app = create_app("config.MockConfig")
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "igor",
            "last_name": "primo",
            "cpf": "427.510.852-37",
            "email": "igorprimo62@gmail.com",
            "birth_date": "1999-10-20",
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "igor",
            "last_name": "primo",
            "cpf": "42751085232",
            "email": "igorprimo62@gmail.com",
            "birth_date": "1999-10-20",
        }

    def test_get_users(self, client):
        response = client.get("/users")
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post("/user", json=valid_user)
        assert response.status_code == 200
        assert b"successfully" in response.data

        response = client.post("/user", json=invalid_user)
        assert response.status_code == 400
        assert b"invalid" in response.data
