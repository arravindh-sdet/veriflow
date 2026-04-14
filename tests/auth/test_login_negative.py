import json
import logging
import allure
import pytest

from utilities.payloads.auth.auth_endpoints import AuthEndpoints
from utilities.payloads.auth.login_payloads import LoginPayload

logger = logging.getLogger(__name__)

@allure.feature("Auth")
@allure.story("Login Negative")
def test_login_invalid_username(api_client):
    case_name, payload = LoginPayload.invalid_username()

    logger.info(f"{case_name}\n{json.dumps(payload, indent=2)}")
    response = api_client.post(AuthEndpoints.login(), json=payload)

    assert response.status_code == 401


@allure.feature("Auth")
@allure.story("Login Negative")
def test_login_invalid_password(api_client):
    case_name, payload = LoginPayload.invalid_password()

    logger.info(f"{case_name}\n{json.dumps(payload, indent=2)}")
    response = api_client.post(AuthEndpoints.login(), json=payload)

    assert response.status_code == 401


@allure.feature("Auth")
@allure.story("Login Negative")
@pytest.mark.parametrize(
    "case_name,payload",
    LoginPayload.empty_credentials()
)
def test_login_empty_credentials(api_client, case_name, payload):
    logger.info(f"{case_name}\n{json.dumps(payload, indent=2)}")

    response = api_client.post(AuthEndpoints.login(), json=payload)
    assert response.status_code == 400


@allure.feature("Auth")
@allure.story("Login Negative")
@pytest.mark.parametrize(
    "case_name,payload",
    LoginPayload.malformed_payload()
)
def test_login_malformed_payload(api_client, case_name, payload):
    logger.info(f"{case_name}\n{json.dumps(payload, indent=2)}")

    response = api_client.post(AuthEndpoints.login(), json=payload)
    assert response.status_code == 400


@allure.feature("Auth")
@allure.story("Login Negative")
def test_login_inactive_user(api_client):
    case_name, payload = LoginPayload.inactive_user()

    logger.info(f"{case_name}\n{json.dumps(payload, indent=2)}")
    response = api_client.post(AuthEndpoints.login(), json=payload)

    assert response.status_code == 403


@allure.feature("Auth")
@allure.story("Authorization")
def test_request_without_token(api_client):
    api_client.headers.pop("Authorization", None)

    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 401


@allure.feature("Auth")
@allure.story("Authorization")
def test_request_with_expired_token(api_client):
    api_client.headers["Authorization"] = "Bearer expired.jwt.token"

    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 401


@allure.feature("Auth")
@allure.story("Authorization")
def test_request_with_invalid_token(api_client):
    api_client.headers["Authorization"] = "Bearer invalid_or_tampered_token"

    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 401



# @allure.feature("Auth")
# @allure.story("Refresh Token Negative")
# def test_refresh_token_invalid(api_client):
#     payload = RefreshPayload.invalid()
#
#     logger.info(json.dumps(payload, indent=2))
#
#     response = api_client.post(
#         AuthEndpoints.refresh_token(),
#         json=payload,
#         auth_required=False
#     )
#
#     assert response.status_code == 401
