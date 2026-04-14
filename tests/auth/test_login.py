import pytest

@pytest.mark.order(1)
def test_login(auth_tokens):
    # print(auth_tokens)

    assert "access_token" in auth_tokens
    assert "refresh_token" in auth_tokens

    print("access_token:", auth_tokens["access_token"])
    print("refresh_token:", auth_tokens["refresh_token"])






