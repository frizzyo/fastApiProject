from app.services.auth import AuthService


def test_create_access_token():
    data = {"user_id": 666}
    jwt_token = AuthService().create_access_token(data=data)

    assert jwt_token
    assert isinstance(jwt_token, str)
