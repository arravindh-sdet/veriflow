import pytest
from core.config_loader import load_config
from core.auth import login
from core.api_client import APIClient

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against: dev / qa / prod"
    )

@pytest.fixture(scope="session")
def config(request):
    """Load environment config once."""
    env = request.config.getoption("--env")
    return load_config(env)

@pytest.fixture(scope="session")
def auth_tokens(config):
    """Perform login once and return tokens."""
    creds = config["credentials"]

    tokens = login(
        base_url=config["base_url"],
        endpoint=config["login_endpoint"],
        username=creds["email"],
        password=creds["password"]
    )

    return tokens

@pytest.fixture(scope="session")
def api_client(config, auth_tokens):
    """Provide a reusable authenticated API client."""
    # Define a login function compatible with APIClient
    def login_func():
        return login(
            base_url=config["base_url"],
            endpoint=config["login_endpoint"],
            username=config["credentials"]["email"],
            password=config["credentials"]["password"]
        )

    client = APIClient(
        base_url=config["base_url"],
        access_token=auth_tokens["access_token"],
        refresh_token=auth_tokens["refresh_token"],
        login_func=login_func,
        refresh_endpoint=config.get("refresh_endpoint", "/api/v1/user/create/refreshToken")
    )
    return client

@pytest.fixture(scope="session")
def access_token(auth_tokens):
    return auth_tokens["access_token"]

@pytest.fixture(scope="session")
def refresh_token(auth_tokens):
    return auth_tokens["refresh_token"]
