# COMS Pytest - API and UI Testing Framework

A comprehensive pytest-based API and UI testing framework with advanced features including authentication, token refresh, Playwright UI automation, allure reporting, and schema validation.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Core Components](#core-components)
- [Testing Guide](#testing-guide)
- [Reporting](#reporting)
- [Contributing](#contributing)

---

## Overview

COMS Pytest is a modern API and UI testing framework built with:

- **pytest** - Python testing framework
- **requests** - HTTP client library
- **Playwright** - Browser automation for UI testing
- **allure-pytest** - Beautiful test reporting
- **jsonschema** - JSON schema validation
- **PyYAML** - Configuration management

### Key Features

✅ Automated authentication and token management  
✅ Automatic token refresh on expiration  
✅ Centralized configuration via YAML  
✅ Schema validation for API responses  
✅ Playwright-powered UI smoke and interaction tests  
✅ Beautiful Allure HTML reports  
✅ Organized test suites by feature  
✅ Request/response logging  
✅ Parametrized test cases  

---

## Project Structure

```
COMS_Pytest/
├── config/                          # Configuration files
│   ├── dev.yaml                    # Development environment config
│   └── __init__.py
│
├── core/                            # Core framework components
│   ├── api_client.py               # Main API client with token refresh
│   ├── auth.py                     # Authentication logic
│   ├── config_loader.py            # YAML config loader
│   └── __init__.py
│
├── helpers/                         # Helper utilities
│   ├── validators/
│   │   ├── schema_validator.py     # JSON schema validation
│   │   ├── pagination_validator.py # Pagination validation
│   │   └── __init__.py
│   ├── wrappers/
│   │   ├── organization_wrapper.py # Response wrapper classes
│   │   └── __init__.py
│   └── __init__.py
│
├── utilities/                       # Test utilities & payloads
│   ├── organization_schema.py      # Schema definitions
│   ├── payloads/
│   │   ├── auth/                   # Auth payloads
│   │   ├── organization/           # Organization payloads
│   │   └── __init__.py
│   └── __init__.py
│
├── tests/                           # Test suites
│   ├── auth/
│   │   ├── test_login.py           # Login tests
│   │   ├── test_login_negative.py  # Negative login tests
│   │   └── __init__.py
│   ├── organisation/
│   │   ├── test_organization.py    # Organization API tests
│   │   ├── test_org_pagination.py  # Organization pagination tests
│   │   └── __init__.py
│   └── __init__.py
│
├── conftest.py                      # Pytest fixtures & configuration
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Python dependencies
├── ui/                              # Playwright page objects
│   └── pages/
│       ├── base_page.py             # Shared page helpers
│       └── demo_page.py             # Demo UI page object
│
├── tests/ui/                        # UI test suites
│   ├── fixtures/demo_app.html       # Local demo page for Playwright
│   ├── test_demo_page.py            # Self-contained UI tests
│   └── test_live_ui_smoke.py        # Real app smoke test pattern
│
├── reports/                         # HTML test reports
├── allure-results/                  # Allure report data
└── allure-report/                   # Generated Allure HTML report
```

---

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd COMS_Pytest
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers** (required for UI tests)
   ```bash
   python -m playwright install chromium
   ```

5. **Install Allure** (optional, for enhanced reporting)
   ```bash
   # macOS
   brew install allure

   # Ubuntu/Debian
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure

   # Or install via pip
   pip install allure-pytest
   ```

---

## Configuration

### Environment Configuration

Configuration files are located in the `config/` directory. Each environment has its own YAML file.

#### `config/dev.yaml`

```yaml
base_url: "https://api.example.com"
ui_base_url: ""
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  email: "your-email@example.com"
  password: "your-password"
```

For personal credentials, create `config/dev.local.yaml`. The loader will use that private file automatically when it exists, and `.gitignore` keeps it out of git.

### Configuration Fields

| Field | Description | Example |
|-------|-------------|---------|
| `base_url` | API base URL | `https://api.example.com` |
| `ui_base_url` | UI base URL for Playwright tests | `https://app.example.com` |
| `login_endpoint` | Authentication endpoint | `/api/v1/auth/login` |
| `refresh_endpoint` | Token refresh endpoint | `/api/v1/auth/refresh` |
| `credentials.email` | User email for login | `user@example.com` |
| `credentials.password` | User password | `password123` |

### Adding New Environments

1. Create a new YAML file in `config/` (e.g., `qa.yaml`, `prod.yaml`)
2. Add the same structure with environment-specific values
3. Run tests with `--env qa` or `--env prod`

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with specific environment
pytest --env dev
pytest --env qa
pytest --env prod

# Run specific test file
pytest tests/auth/test_login.py

# Run specific test function
pytest tests/auth/test_login.py::test_login

# Run Playwright UI demo tests
pytest tests/ui/test_demo_page.py -m ui

# Run live UI smoke test against a real app
pytest tests/ui/test_live_ui_smoke.py -m ui --ui-base-url https://your-ui-app.com

# Run tests with specific marker
pytest -m "order(1)"

# Run tests verbosely
pytest -v

# Run with logs
pytest -s

# Run UI tests in headed mode
pytest tests/ui -m ui --headed
```

### Advanced Options

```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate Allure report
pytest --alluredir=allure-results

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto

# Run specific test by keyword
pytest -k "login"

# Run tests and stop on first failure
pytest -x

# Run tests and stop after N failures
pytest --maxfail=3

# Show test durations
pytest --durations=10
```

### Running Allure Reports

```bash
# Generate Allure report
pytest --alluredir=allure-results

# View Allure report in browser
allure serve allure-results
```

---

## Core Components

### 1. API Client (`core/api_client.py`)

The main API client class handling all HTTP requests with automatic token management.

#### Features

- ✅ Automatic token refresh on 401 errors
- ✅ Request/response logging with Allure
- ✅ Custom header support
- ✅ Fallback to login on refresh failure
- ✅ Pretty JSON logging

#### Usage

```python
from core.api_client import APIClient

# Initialize
client = APIClient(
    base_url="https://api.example.com",
    access_token="token",
    refresh_token="refresh_token",
    refresh_endpoint="/api/v1/user/refreshToken",
    login_func=login_function
)

# Make requests
response = client.get("/api/v1/organizations")
response = client.post("/api/v1/organizations", json={"name": "Org"})
response = client.put("/api/v1/organizations/123", json={"name": "New Name"})
response = client.delete("/api/v1/organizations/123")
```

#### Key Methods

| Method | Description |
|--------|-------------|
| `get(endpoint, params, headers)` | GET request |
| `post(endpoint, json, headers, auth_required)` | POST request |
| `put(endpoint, json, headers)` | PUT request |
| `patch(endpoint, json, headers)` | PATCH request |
| `delete(endpoint, headers)` | DELETE request |

### 2. Authentication (`core/auth.py`)

Handles user authentication and token retrieval.

```python
from core.auth import login

tokens = login(
    base_url="https://api.example.com",
    endpoint="/api/v1/user/login",
    username="user@example.com",
    password="password123"
)

# Returns
{
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc..."
}
```

### 3. Configuration Loader (`core/config_loader.py`)

Loads environment-specific configuration from YAML files.

```python
from core.config_loader import load_config

# Load config for dev environment
config = load_config("dev")

# Access config values
base_url = config["base_url"]
creds = config["credentials"]
```

### 4. Fixtures (`conftest.py`)

Pytest fixtures for common setup tasks.

#### Available Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `config` | session | Environment configuration |
| `auth_tokens` | session | Authentication tokens |
| `api_client` | session | Authenticated API client |
| `access_token` | session | Access token string |
| `refresh_token` | session | Refresh token string |

#### Example Usage

```python
def test_create_organization(api_client):
    response = api_client.post(
        "/api/v1/organizations",
        json={"name": "Test Org"}
    )
    assert response.status_code == 200
```

---

## Testing Guide

### Writing Tests

#### Basic Test Structure

```python
import pytest
import allure
from helpers.validators.schema_validator import validate_schema

@allure.feature("Organization")
@allure.story("Create")
def test_create_org(api_client):
    # Arrange
    payload = {"name": "Test Organization"}
    
    # Act
    response = api_client.post("/api/v1/organizations", json=payload)
    
    # Assert
    assert response.status_code == 200
    validate_schema(response.json(), ORGANIZATION_SCHEMA)
```

### Parametrized Tests

```python
@pytest.mark.parametrize(
    "case_name,payload",
    [
        ("valid_data", {"name": "Org1"}),
        ("another_valid", {"name": "Org2"})
    ]
)
def test_multiple_cases(api_client, case_name, payload):
    response = api_client.post("/api/v1/organizations", json=payload)
    assert response.status_code == 200
```

### Test Ordering

```python
import pytest

@pytest.mark.order(1)
def test_login_first(auth_tokens):
    assert auth_tokens["access_token"]

@pytest.mark.order(2)
def test_create_org_second(api_client):
    response = api_client.post("/api/v1/organizations", json={})
    assert response.status_code == 200
```

### Using Allure Decorators

```python
@allure.feature("Organization")           # Feature name
@allure.story("Create")                   # Story name
@allure.title("Create Organization")      # Test title
@allure.description("Creates a new org")  # Test description
@allure.severity(allure.severity_level.CRITICAL)  # Severity
def test_example(api_client):
    pass
```

### Schema Validation

```python
from helpers.validators.schema_validator import validate_schema
from utilities.organization_schema import ORGANIZATION_SCHEMA

def test_org_schema(api_client):
    response = api_client.get("/api/v1/organizations/123")
    
    # Validate response against schema
    validate_schema(response.json(), ORGANIZATION_SCHEMA)
```

### Response Wrapping

```python
from helpers.wrappers.organization_wrapper import ResponseWrapper

def test_org_wrapper(api_client):
    response = api_client.get("/api/v1/organizations/123")
    
    # Wrap response for easy access
    wrapped = ResponseWrapper(response.json())
    org_id = wrapped.responseObject.organizationId
    assert org_id
```

---

## Token Refresh Flow

### How Token Refresh Works

1. **Request Made**: API client makes a request with current access token
2. **401 Received**: If server returns 401 (Unauthorized)
3. **Automatic Refresh**: Client attempts to refresh token using refresh token
4. **New Headers**: Retries request with new access token
5. **Success/Fallback**: On success, continues; on failure, attempts login

### Configuration

Token refresh is automatically configured in `conftest.py`:

```python
@pytest.fixture(scope="session")
def api_client(config, auth_tokens):
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
```

### Testing Token Expiration

To test token refresh functionality:

```python
@pytest.mark.order(1)
def test_login(auth_tokens):
    assert auth_tokens["access_token"]
    assert auth_tokens["refresh_token"]

def test_with_expired_token(api_client):
    # Use an expired token to test refresh
    api_client.token_store["access_token"] = "expired_token"
    
    # Make request - should trigger refresh
    response = api_client.get("/api/v1/organizations")
    
    # Request should succeed if refresh works
    assert response.status_code == 200
```

---

## Reporting

### HTML Reports

Reports are automatically generated in `reports/report.html`

```bash
pytest --html=reports/report.html --self-contained-html
```

### Allure Reports

Allure provides beautiful, interactive test reports.

#### Generate Report

```bash
# Run tests with Allure
pytest --alluredir=allure-results

# Generate and view report
allure serve allure-results
```

#### Report Features

- 📊 Test statistics and trends
- 🎯 Failure analysis
- ⏱️ Test duration tracking
- 📎 Attachments (logs, screenshots)
- 🏷️ Tags and categories
- 📈 Historical trends

### Allure Annotations

```python
@allure.feature("Feature Name")
@allure.story("Story Name")
@allure.title("Test Title")
@allure.description("Detailed description")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com", name="Related Link")
def test_example():
    pass
```

---

## Validators

### Schema Validator

Validates JSON responses against predefined schemas.

```python
from helpers.validators.schema_validator import validate_schema

# Validate
validate_schema(response_data, schema)

# Raises AssertionError if invalid
```

### Pagination Validator

Validates pagination in responses.

```python
from helpers.validators.pagination_validator import validate_pagination

validate_pagination(response_data)
```

---

## Best Practices

### 1. Test Organization

```
tests/
├── feature1/
│   ├── test_crud.py
│   ├── test_validation.py
│   └── test_edge_cases.py
├── feature2/
│   ├── test_feature2.py
│   └── __init__.py
└── __init__.py
```

### 2. Naming Conventions

- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_description`
- Fixtures: Use descriptive names
- Classes: `Test*`

### 3. Test Independence

- Each test should be independent
- Use `@pytest.mark.order()` if tests depend on others
- Clean up after each test if needed

### 4. Assertions

```python
# Good
assert response.status_code == 200
assert "access_token" in response_data

# Avoid
assert response  # Vague
assert response.status_code  # Doesn't check value
```

### 5. Use Fixtures

```python
# Good
def test_something(api_client, auth_tokens):
    pass

# Avoid
def test_something():
    client = APIClient(...)  # Creates new client each time
    pass
```

### 6. Meaningful Test Data

```python
# Good
payload = {
    "name": "Valid Organization",
    "email": "org@example.com"
}

# Avoid
payload = {"name": "a", "email": "e@e.com"}
```

---

## Troubleshooting

### Common Issues

#### 1. Token Refresh Not Working

**Problem**: Tests fail with 401 errors

**Solution**:
- Check `refresh_endpoint` in config
- Verify refresh token is valid
- Check token payload format

```python
# Debug token storage
print(client.token_store)
```

#### 2. Config File Not Found

**Problem**: `FileNotFoundError: Config file not found`

**Solution**:
- Ensure config file exists in `config/` directory
- Run tests from project root
- Use correct environment name

```bash
pytest --env dev  # Uses config/dev.yaml
```

#### 3. Authentication Failure

**Problem**: Login tests fail

**Solution**:
- Verify credentials in config
- Check endpoint URL
- Ensure API is accessible

#### 4. Schema Validation Errors

**Problem**: Schema validation fails

**Solution**:
- Check schema definition
- Verify response structure
- Update schema if API changed

---

## Contributing

### Adding New Tests

1. Create test file in `tests/feature/` directory
2. Use descriptive names
3. Add Allure decorators
4. Include docstrings
5. Run tests locally

### Adding New Fixtures

1. Add to `conftest.py`
2. Use appropriate scope
3. Include docstring
4. Export if needed by other modules

### Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings
- Keep functions focused

---

## Useful Commands

```bash
# Run all tests
pytest

# Run with specific environment
pytest --env dev

# Run specific test
pytest tests/auth/test_login.py::test_login

# Run with coverage
pytest --cov=core tests/

# Generate reports
pytest --html=reports/report.html --alluredir=allure-results

# View allure report
allure serve allure-results

# List all tests
pytest --collect-only

# Run tests matching pattern
pytest -k "login"

# Run with markers
pytest -m "order(1)"

# Verbose output
pytest -v -s

# Show print statements
pytest -s
```

---

## API Endpoints Reference

### Authentication

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/user/create/login` | POST | User login |
| `/api/v1/user/create/refreshToken` | POST | Refresh access token |

### Organization

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/organizations/create` | POST | Create organization |
| `/api/v1/organizations` | GET | List organizations |
| `/api/v1/organizations/{id}` | GET | Get organization |
| `/api/v1/organizations/{id}` | PUT | Update organization |
| `/api/v1/organizations/{id}` | DELETE | Delete organization |

---

## Support & Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **Requests Library**: https://docs.python-requests.org/
- **Allure Documentation**: https://docs.qameta.io/allure/
- **JSONSchema**: https://json-schema.org/
- **PyYAML**: https://pyyaml.org/

---

## License

[Specify your license here]

---

## Contact

For questions or issues, contact the development team.

---

**Last Updated**: March 17, 2026  
**Version**: 1.0.0
