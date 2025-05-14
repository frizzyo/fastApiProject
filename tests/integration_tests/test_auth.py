from app.services.auth import AuthService


def test_decode_and_encode_access_token():
    data = {"user_id": 666}
    jwt_token = AuthService().create_access_token(data=data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    encode_data = AuthService().decode_token(jwt_token)

    assert encode_data
    assert encode_data["user_id"] == data["user_id"]
