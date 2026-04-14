from pathlib import Path

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
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser for Playwright UI tests: chromium / firefox / webkit"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Playwright UI tests in headed mode"
    )
    parser.addoption(
        "--ui-base-url",
        action="store",
        default=None,
        help="Base URL for UI tests. Overrides ui_base_url from the config file."
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "ui: marks Playwright-based UI tests")


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


@pytest.fixture(scope="session")
def ui_base_url(request, config):
    """Return a UI base URL from CLI or config, if one is configured."""
    cli_value = request.config.getoption("--ui-base-url")
    return cli_value if cli_value is not None else config.get("ui_base_url", "")


@pytest.fixture(scope="session")
def playwright_driver():
    """Start Playwright only when a UI fixture requests it."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        pytest.skip(
            "Playwright is not installed. Run `pip install -r requirements.txt` "
            "and `python -m playwright install chromium` before running UI tests."
        )

    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def ui_browser(playwright_driver, request):
    """Launch a shared browser instance for UI tests."""
    browser_name = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")

    if browser_name not in {"chromium", "firefox", "webkit"}:
        raise pytest.UsageError(
            f"Unsupported browser '{browser_name}'. Use chromium, firefox, or webkit."
        )

    browser_launcher = getattr(playwright_driver, browser_name)
    browser = browser_launcher.launch(headless=not headed)
    yield browser
    browser.close()


@pytest.fixture
def ui_context(ui_browser):
    """Provide an isolated browser context per test."""
    context = ui_browser.new_context(viewport={"width": 1440, "height": 900})
    yield context
    context.close()


@pytest.fixture
def ui_page(ui_context):
    """Provide a Playwright page for UI interactions."""
    page = ui_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def demo_ui_url():
    """Return the local demo page URL used by the sample Playwright tests."""
    demo_page_path = Path(__file__).resolve().parent / "tests" / "ui" / "fixtures" / "demo_app.html"
    return demo_page_path.resolve().as_uri()
