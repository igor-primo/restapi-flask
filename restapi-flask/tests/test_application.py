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

    def test_get_user(self, client, valid_user, invalid_user):
        response = client.get("/user/%s" % valid_user["cpf"])
        assert response.status_code == 200
        assert response.json[0]["first_name"] == "igor"
        assert response.json[0]["last_name"] == "primo"
        assert response.json[0]["cpf"] == "427.510.852-37"
        assert response.json[0]["email"] == "igorprimo62@gmail.com"
        assert response.json[0]["birth_date"]["$date"] == "1999-10-20T00:00:00Z"

        response = client.get("/user/%s" % invalid_user["cpf"])
        assert response.status_code == 400
        assert b"User does not exist in database" in response.data

    def test_patch_user(self, client, valid_user):
        valid_user["first_name"] = "igorr"
        response = client.patch("/user", json=valid_user)
        assert response.status_code == 200
        assert b"User updated" in response.data

        valid_user["cpf"] = "427.510.852-38"
        response = client.patch("/user", json=valid_user)
        assert response.status_code == 400
        assert b"does not exist in database" in response.data

    def test_delete_user(self, client, valid_user, invalid_user):
        response = client.delete("/user/%s" % valid_user["cpf"])
        assert response.status_code == 200
        assert b"deleted" in response.data

        response = client.delete("/user/%s" % valid_user["cpf"])
        assert response.status_code == 400
        assert b"does not exist in database" in response.data
