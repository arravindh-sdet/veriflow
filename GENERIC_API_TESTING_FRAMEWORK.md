# API Testing Framework - Complete Documentation

**Version**: 1.0.0  
**Last Updated**: March 17, 2026  
**Documentation Type**: Universal API Testing Framework Guide

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Installation & Setup](#installation--setup)
4. [Quick Start (5 Minutes)](#quick-start-5-minutes)
5. [Project Structure](#project-structure)
6. [Core Components](#core-components)
7. [Configuration Guide](#configuration-guide)
8. [Running Tests](#running-tests)
9. [Testing Guide](#testing-guide)
10. [API Client Reference](#api-client-reference)
11. [Authentication & Token Management](#authentication--token-management)
12. [Fixtures Reference](#fixtures-reference)
13. [Best Practices](#best-practices)
14. [Troubleshooting](#troubleshooting)
15. [API Endpoints Reference](#api-endpoints-reference)
16. [Command Reference](#command-reference)
17. [FAQ](#faq)

---

## Executive Summary

This is a modern, comprehensive API testing framework built with pytest, offering:

- ✅ **Automated Authentication** - Automatic login and token management
- ✅ **Automatic Token Refresh** - Seamless token refresh on expiration
- ✅ **Centralized Configuration** - YAML-based environment management
- ✅ **Schema Validation** - JSON schema validation for responses
- ✅ **Beautiful Reporting** - HTML reports with trends
- ✅ **Organized Tests** - Feature-based test organization
- ✅ **Request Logging** - Complete request/response logging
- ✅ **Parametrized Tests** - Data-driven testing capabilities

---

## Project Overview

### What is This Framework?

This is an enterprise-grade API testing framework designed to simplify test creation and maintenance. It provides automatic authentication, token management, and comprehensive reporting capabilities for testing any REST/HTTP API.

### Key Technologies

| Technology | Purpose | Version |
|-----------|---------|---------|
| pytest | Testing framework | Latest |
| requests | HTTP client | Latest |
| PyYAML | Configuration | Latest |
| allure-pytest | Test reporting | Latest |
| jsonschema | Schema validation | Latest |

### Core Features

1. **Automatic Authentication**
   - Automatic login on test start
   - Session-scoped token reuse
   - Fallback mechanisms

2. **Token Management**
   - Automatic token refresh on 401
   - Refresh token handling
   - Token storage and retrieval

3. **Configuration Management**
   - YAML-based configuration
   - Multiple environments (dev, qa, prod)
   - Environment-specific settings

4. **Testing Features**
   - Parametrized tests
   - Test ordering
   - Fixtures for common setup
   - Schema validation

5. **Reporting**
   - HTML reports
   - Allure reports with trends
   - Request/response logging
   - Test history

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Step-by-Step Installation

#### 1. Clone Repository

```bash
git clone <repository-url>
cd <project-directory>
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Or Windows
.venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Verify Installation

```bash
pytest --version
```

### Required Dependencies

```
allure-python-commons
pytest
requests
PyYAML
pytest-order
pytest-html
jsonschema
allure-pytest
```

---

## Quick Start (5 Minutes)

### 1. Installation (1 minute)

```bash
pip install -r requirements.txt
```

### 2. Configure Your Environment (1 minute)

Edit `config/dev.yaml`:

```yaml
base_url: "https://your-api.com"
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  username: "test-user"
  password: "test-password"
```

### 3. Run Your First Test (1 minute)

```bash
pytest tests/auth/test_login.py -v
```

### 4. View Results (2 minutes)

```bash
# View HTML report
open reports/report.html

# Or generate Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Project Structure

```
project-root/
├── config/                          # Configuration files
│   ├── dev.yaml                    # Development config
│   ├── qa.yaml                     # QA config
│   ├── prod.yaml                   # Production config
│   └── __init__.py
│
├── core/                            # Core framework
│   ├── api_client.py               # API client with token refresh
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
│   │   ├── response_wrapper.py     # Response wrappers
│   │   └── __init__.py
│   └── __init__.py
│
├── utilities/                       # Test utilities
│   ├── schemas/
│   │   ├── api_schema.py           # Schema definitions
│   │   └── __init__.py
│   ├── payloads/
│   │   ├── auth/                   # Auth payloads
│   │   ├── resources/              # Resource payloads
│   │   └── __init__.py
│   └── __init__.py
│
├── tests/                           # Test suites
│   ├── auth/
│   │   ├── test_login.py           # Login tests
│   │   ├── test_login_negative.py  # Negative tests
│   │   └── __init__.py
│   ├── api/
│   │   ├── test_api_crud.py        # CRUD tests
│   │   ├── test_api_validation.py  # Validation tests
│   │   └── __init__.py
│   └── __init__.py
│
├── conftest.py                      # Pytest fixtures
├── pytest.ini                       # Pytest config
├── requirements.txt                 # Dependencies
├── reports/                         # HTML reports
├── allure-results/                  # Allure data
└── allure-report/                   # Allure HTML
```

---

## Core Components

### 1. API Client (`core/api_client.py`)

The main class for making HTTP requests with automatic token management.

#### Features
- Automatic token refresh on 401
- Request/response logging
- Custom header support
- Fallback to login on refresh failure

#### Initialization

```python
from core.api_client import APIClient

client = APIClient(
    base_url="https://api.example.com",
    access_token="token",
    refresh_token="refresh_token",
    refresh_endpoint="/api/v1/auth/refresh",
    login_func=login_function
)
```

#### HTTP Methods

```python
# GET
response = client.get("/api/v1/data")
response = client.get("/api/v1/data", params={"page": 1})

# POST
response = client.post("/api/v1/data", json={"name": "value"})

# PUT
response = client.put("/api/v1/data/123", json={"name": "updated"})

# PATCH
response = client.patch("/api/v1/data/123", json={"status": "active"})

# DELETE
response = client.delete("/api/v1/data/123")
```

#### Token Management

Tokens are automatically stored and managed:

```python
# Access tokens
client.token_store["access_token"]  # Current access token
client.token_store["refresh_token"]  # Current refresh token

# Update tokens
client.token_store["access_token"] = "new_token"
```

#### Error Handling

```python
try:
    response = client.get("/api/v1/data")
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.Timeout:
    print("Request timed out")
```

### 2. Authentication (`core/auth.py`)

Handles user login and token retrieval.

```python
from core.auth import login

tokens = login(
    base_url="https://api.example.com",
    endpoint="/api/v1/auth/login",
    username="user",
    password="password"
)

# Returns: {"access_token": "...", "refresh_token": "..."}
```

### 3. Configuration Loader (`core/config_loader.py`)

Loads YAML configuration files.

```python
from core.config_loader import load_config

# Load config
config = load_config("dev")

# Access values
base_url = config["base_url"]
username = config["credentials"]["username"]
timeout = config.get("timeout", 30)
```

---

## Configuration Guide

### Configuration Structure

All configurations are YAML files in the `config/` directory.

#### YAML Format

```yaml
base_url: "https://api.example.com"
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  username: "test-user"
  password: "test-password"
timeout: 30
verify_ssl: true
```

### Configuration Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `base_url` | Yes | API base URL | `https://api.example.com` |
| `login_endpoint` | Yes | Login endpoint | `/api/v1/auth/login` |
| `refresh_endpoint` | Yes | Token refresh endpoint | `/api/v1/auth/refresh` |
| `credentials.username` | Yes | Username | `test-user` |
| `credentials.password` | Yes | Password | `test-password` |
| `timeout` | No | Request timeout (seconds) | `30` |
| `verify_ssl` | No | Verify SSL certificates | `true` |

### Environment Configurations

#### Development (dev.yaml)

```yaml
base_url: "https://dev-api.example.com"
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  username: "dev-user"
  password: "dev-password"
```

#### QA (qa.yaml)

```yaml
base_url: "https://qa-api.example.com"
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  username: "qa-user"
  password: "qa-password"
verify_ssl: true
timeout: 30
```

#### Production (prod.yaml)

```yaml
base_url: "https://api.example.com"
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  username: "prod-user"
  password: "prod-password"
verify_ssl: true
timeout: 60
```

### Creating New Environment

1. Create new YAML file:
   ```bash
   touch config/staging.yaml
   ```

2. Add configuration:
   ```yaml
   base_url: "https://staging-api.example.com"
   # ... rest of config
   ```

3. Use in tests:
   ```bash
   pytest --env staging
   ```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with environment
pytest --env dev
pytest --env qa
pytest --env prod

# Run specific file
pytest tests/auth/test_login.py

# Run specific test
pytest tests/auth/test_login.py::test_login

# Run tests matching pattern
pytest -k "login"

# Verbose output
pytest -v

# Show print statements
pytest -s

# Verbose with output
pytest -v -s
```

### Advanced Options

```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate Allure report
pytest --alluredir=allure-results

# View Allure report
allure serve allure-results

# Run specific markers
pytest -m "order(1)"

# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Show test durations
pytest --durations=10

# Run with debug logging
pytest --log-cli-level=DEBUG
```

---

## Testing Guide

### Test Structure

#### Basic Test

```python
import pytest

def test_authentication(auth_tokens):
    """Test authentication process."""
    assert "access_token" in auth_tokens
    assert "refresh_token" in auth_tokens
```

#### AAA Pattern (Arrange-Act-Assert)

```python
def test_create_data(api_client):
    # Arrange: Prepare test data
    payload = {
        "name": "Test Data",
        "value": "test-value"
    }
    
    # Act: Perform action
    response = api_client.post("/api/v1/data", json=payload)
    
    # Assert: Verify results
    assert response.status_code == 200
    assert "dataId" in response.json()["data"]
```

### Response Assertions

```python
def test_response_validation(api_client):
    response = api_client.get("/api/v1/data")
    
    # Status code
    assert response.status_code == 200
    
    # Response headers
    assert response.headers["Content-Type"] == "application/json"
    
    # Response content
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
```

### Parametrized Tests

```python
@pytest.mark.parametrize(
    "test_data",
    ["Data1", "Data2", "Data3"]
)
def test_multiple_operations(api_client, test_data):
    response = api_client.post(
        "/api/v1/data",
        json={"name": test_data}
    )
    assert response.status_code == 200
```

### Test Ordering

```python
import pytest

@pytest.mark.order(1)
def test_login_first(auth_tokens):
    """This test runs first."""
    assert auth_tokens["access_token"]

@pytest.mark.order(2)
def test_api_operations_second(api_client):
    """This test runs second."""
    response = api_client.post("/api/v1/data", json={})
    assert response.status_code == 200
```

### Using Allure Decorators

```python
import allure

@allure.feature("Data Operations")
@allure.story("Create")
@allure.title("Create new data item")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_data(api_client):
    response = api_client.post("/api/v1/data", json={"name": "Test"})
    assert response.status_code == 200
```

#### Allure Steps

```python
def test_workflow(api_client):
    with allure.step("Create data"):
        response = api_client.post(
            "/api/v1/data",
            json={"name": "Test"}
        )
        assert response.status_code == 200
        data_id = response.json()["data"]["dataId"]
    
    with allure.step("Retrieve data"):
        response = api_client.get(f"/api/v1/data/{data_id}")
        assert response.status_code == 200
```

### Schema Validation

```python
from helpers.validators.schema_validator import validate_schema
from utilities.schemas.api_schema import DATA_SCHEMA

def test_schema_validation(api_client):
    response = api_client.get("/api/v1/data/123")
    
    # Validate response against schema
    validate_schema(response.json(), DATA_SCHEMA)
```

### Response Wrapping

```python
from helpers.wrappers.response_wrapper import ResponseWrapper

def test_response_wrapper(api_client):
    response = api_client.get("/api/v1/data/123")
    
    # Easy access to nested fields
    wrapped = ResponseWrapper(response.json())
    data_id = wrapped.data.dataId
    assert data_id
```

---

## API Client Reference

### Public Methods

#### GET Request

```python
get(endpoint: str, params: dict = None, headers: dict = None) -> requests.Response
```

**Example**:
```python
response = client.get("/api/v1/data")
response = client.get("/api/v1/data", params={"page": 1})
response = client.get("/api/v1/data", headers={"X-Custom": "value"})
```

#### POST Request

```python
post(endpoint: str, json: dict = None, headers: dict = None, auth_required: bool = True) -> requests.Response
```

**Example**:
```python
payload = {"name": "New Data"}
response = client.post("/api/v1/data", json=payload)
response = client.post("/api/v1/auth/login", json=creds, auth_required=False)
```

#### PUT Request

```python
put(endpoint: str, json: dict = None, headers: dict = None) -> requests.Response
```

**Example**:
```python
response = client.put(
    "/api/v1/data/123",
    json={"name": "Updated"}
)
```

#### PATCH Request

```python
patch(endpoint: str, json: dict = None, headers: dict = None) -> requests.Response
```

**Example**:
```python
response = client.patch(
    "/api/v1/data/123",
    json={"status": "active"}
)
```

#### DELETE Request

```python
delete(endpoint: str, headers: dict = None) -> requests.Response
```

**Example**:
```python
response = client.delete("/api/v1/data/123")
```

### Private Methods

#### _refresh_access_token()

Attempts to refresh the access token using refresh token.

```python
success = client._refresh_access_token()  # Returns: bool
```

#### _login()

Attempts to log in using the login function.

```python
success = client._login()  # Returns: bool
```

#### _prepare_headers()

Prepares headers with Bearer token.

```python
headers = client._prepare_headers()
headers = client._prepare_headers({"X-Custom": "value"})
```

---

## Authentication & Token Management

### Token Refresh Flow

```
Request → 401 Response → Refresh Token → New Access Token → Retry Request
                            ↓ (if fails)
                        Fall back to Login
```

### How It Works

1. **Initial Login**: Fixture performs login and gets tokens
2. **Request Made**: APIClient makes request with access token
3. **Token Valid**: Request succeeds
4. **Token Expired**: Server returns 401
5. **Auto Refresh**: APIClient uses refresh token to get new access token
6. **Retry**: Request is retried with new token
7. **Success**: Request succeeds or falls back to login

### Token Structure

Tokens are JWT (JSON Web Tokens):

```
eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2ZDMz...NDA2N30.50KIcIK-NeGmk7TIhYrR4K...
```

Three parts:
- **Header**: Algorithm and token type
- **Payload**: Subject, issued at, expiration
- **Signature**: Cryptographic signature

### Testing Token Refresh

```python
def test_token_refresh(api_client):
    """Token refresh happens automatically."""
    response = api_client.get("/api/v1/data")
    assert response.status_code == 200
```

### Manual Token Operations

```python
# Access tokens
access_token = api_client.token_store["access_token"]
refresh_token = api_client.token_store["refresh_token"]

# Manually refresh
success = api_client._refresh_access_token()

# Manually login
success = api_client._login()

# Update tokens
api_client.token_store["access_token"] = "new_token"
```

### Authorization Headers

Headers are automatically prepared:

```
Authorization: Bearer eyJhbGciOiJIUzUxMiJ9...
Content-Type: application/json
```

---

## Fixtures Reference

### Available Fixtures

All fixtures are in `conftest.py`.

#### config

**Scope**: session  
**Returns**: Configuration dictionary

```python
def test_with_config(config):
    base_url = config["base_url"]
    username = config["credentials"]["username"]
```

#### auth_tokens

**Scope**: session  
**Returns**: Token dictionary

```python
def test_with_tokens(auth_tokens):
    access_token = auth_tokens["access_token"]
    refresh_token = auth_tokens["refresh_token"]
```

#### api_client

**Scope**: session  
**Returns**: Authenticated APIClient instance

```python
def test_with_client(api_client):
    response = api_client.get("/api/v1/data")
```

#### access_token

**Scope**: session  
**Returns**: Access token string

```python
def test_with_access_token(access_token):
    assert access_token.startswith("eyJ")
```

#### refresh_token

**Scope**: session  
**Returns**: Refresh token string

```python
def test_with_refresh_token(refresh_token):
    assert refresh_token.startswith("eyJ")
```

### Creating Custom Fixtures

#### Basic Fixture

```python
@pytest.fixture
def sample_payload():
    """Provides sample payload."""
    return {"name": "Test Data"}

# Use in test
def test_with_payload(api_client, sample_payload):
    response = api_client.post("/api/v1/data", json=sample_payload)
    assert response.status_code == 200
```

#### Fixture with Setup & Teardown

```python
@pytest.fixture
def created_item(api_client):
    """Create item and cleanup after test."""
    # Setup
    response = api_client.post("/api/v1/data", json={"name": "Test"})
    item_id = response.json()["data"]["itemId"]
    
    yield item_id  # Provide to test
    
    # Teardown
    api_client.delete(f"/api/v1/data/{item_id}")

# Use in test
def test_with_created_item(created_item):
    item_id = created_item
    assert item_id
```

#### Parametrized Fixture

```python
@pytest.fixture(params=["Item1", "Item2", "Item3"])
def test_items(request):
    """Parametrized fixture."""
    return request.param

# Test runs once for each parameter
def test_create_items(api_client, test_items):
    response = api_client.post(
        "/api/v1/data",
        json={"name": test_items}
    )
    assert response.status_code == 200
```

#### Fixture Scopes

```python
# Function scope (default) - new for each test
@pytest.fixture(scope="function")
def fresh_data():
    return {"id": 1}

# Module scope - shared by all tests in module
@pytest.fixture(scope="module")
def module_item(api_client):
    response = api_client.post("/api/v1/data", json={})
    return response.json()["data"]["itemId"]

# Session scope - shared by all tests
@pytest.fixture(scope="session")
def session_data():
    return {"data": "shared"}
```

---

## Best Practices

### 1. Test Independence

Each test should be independent:

```python
# Good: Independent tests
def test_create_item_1(api_client):
    response = api_client.post("/api/v1/data", json={"name": "Item1"})
    assert response.status_code == 200

def test_create_item_2(api_client):
    response = api_client.post("/api/v1/data", json={"name": "Item2"})
    assert response.status_code == 200

# Avoid: Dependent tests
def test_create_item():
    # Test 1
    response = api_client.post(...)
    # Test 2 depends on Test 1 output
    response = api_client.get(...)
```

### 2. Clear Assertions

```python
# Good: Specific assertions
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
assert "itemId" in response.json()["data"]

# Avoid: Vague assertions
assert response  # What does this test?
assert response.status_code  # No value check
```

### 3. Descriptive Test Names

```python
# Good: Descriptive names
def test_create_item_with_valid_data():
    pass

def test_create_item_with_missing_name():
    pass

# Avoid: Vague names
def test_item():
    pass

def test_1():
    pass
```

### 4. Use Fixtures

```python
# Good: Use fixtures
def test_example(api_client, config):
    response = api_client.get("/api/v1/data")
    assert config["base_url"] in response.url

# Avoid: Create clients in tests
def test_example():
    client = APIClient(...)  # Don't do this
    response = client.get("/api/v1/data")
```

### 5. Data-Driven Testing

```python
# Good: Parametrized
@pytest.mark.parametrize("item_name", ["Item1", "Item2", "Item3"])
def test_create_items(api_client, item_name):
    response = api_client.post("/api/v1/data", json={"name": item_name})
    assert response.status_code == 200

# Avoid: Hardcoded
def test_create_item_1(api_client):
    response = api_client.post("/api/v1/data", json={"name": "Item1"})
    assert response.status_code == 200

def test_create_item_2(api_client):
    response = api_client.post("/api/v1/data", json={"name": "Item2"})
    assert response.status_code == 200
```

### 6. Schema Validation

```python
from helpers.validators.schema_validator import validate_schema

def test_response_schema(api_client):
    response = api_client.get("/api/v1/data/123")
    validate_schema(response.json(), DATA_SCHEMA)
```

### 7. Meaningful Error Messages

```python
# Good: Clear error messages
if response.status_code != 200:
    print(f"Expected 200 but got {response.status_code}")
    print(f"Response: {response.json()}")

# Show what went wrong
assert response.status_code == 200, \
    f"Request failed: {response.json().get('message')}"
```

### 8. Security Practices

```python
# Never log full tokens
print(f"Token: {token[:20]}...")  # Mask token

# Use environment variables for credentials
import os
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

# Never commit passwords
# Use .gitignore for config files
```

### 9. Logging & Debugging

```python
# Use print statements in tests
def test_example(api_client):
    response = api_client.get("/api/v1/data")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}")
    assert response.status_code == 200

# Run with -s to see output
# pytest tests/file.py -s
```

### 10. Test Organization

```
tests/
├── auth/
│   ├── test_login.py
│   ├── test_login_negative.py
│   └── __init__.py
├── api/
│   ├── test_crud.py
│   ├── test_validation.py
│   ├── test_pagination.py
│   └── __init__.py
└── __init__.py
```

---

## Troubleshooting

### Issue: Config File Not Found

**Error**: `FileNotFoundError: Config file not found: config/dev.yaml`

**Causes**:
- Config file doesn't exist
- Wrong environment name
- Wrong working directory

**Solutions**:
```bash
# Check config files exist
ls config/

# Run from project root
cd /path/to/project

# Use correct environment
pytest --env dev  # Uses config/dev.yaml
```

### Issue: 401 Unauthorized

**Error**: Tests fail with 401 status code

**Causes**:
- Tokens expired and refresh failed
- Invalid credentials
- Refresh endpoint unreachable

**Solutions**:
```bash
# Run login test first
pytest tests/auth/test_login.py -v -s

# Check credentials in config
cat config/dev.yaml

# Verify tokens
pytest -v -s --log-cli-level=DEBUG
```

### Issue: Authentication Failure

**Error**: Login fails with 401

**Causes**:
- Invalid credentials
- Incorrect endpoint URL
- API not accessible

**Solutions**:
```bash
# Check credentials
cat config/dev.yaml

# Test endpoint directly
curl -X POST https://your-api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# Update credentials if needed
# Edit config/dev.yaml with valid credentials
```

### Issue: Import Errors

**Error**: `ModuleNotFoundError: No module named 'pytest'`

**Causes**:
- Virtual environment not activated
- Dependencies not installed

**Solutions**:
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep pytest
```

### Issue: Test Collection Errors

**Error**: No tests found or import errors

**Causes**:
- Test files don't start with `test_`
- Missing `__init__.py` files
- Import errors in test files

**Solutions**:
```bash
# List all collected tests
pytest --collect-only

# Check file naming
ls tests/auth/  # Files should be test_*.py

# Add missing __init__.py
touch tests/__init__.py
touch tests/auth/__init__.py

# Check imports
pytest --tb=short tests/file.py
```

### Issue: Token Refresh Not Working

**Error**: Tests fail with 401 even after refresh

**Causes**:
- Refresh token expired
- Refresh endpoint incorrect
- Server not responding

**Solutions**:
```python
# Check refresh endpoint in config
print(client.refresh_endpoint)

# Check if refresh works manually
success = api_client._refresh_access_token()
print(f"Refresh successful: {success}")

# Check token store
print(f"Access token: {api_client.token_store['access_token'][:20]}...")
```

### Issue: Report Generation Failed

**Error**: HTML report not generated

**Causes**:
- Directory doesn't exist
- Permission denied
- Wrong flag used

**Solutions**:
```bash
# Create reports directory
mkdir -p reports

# Generate with correct flags
pytest --html=reports/report.html --self-contained-html

# Check output
open reports/report.html
```

### Debug Commands

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Very verbose
pytest -vv

# Show test names
pytest -v --collect-only

# Debug with breakpoint
pytest --pdb

# Detailed logging
pytest --log-cli-level=DEBUG

# Specific file
pytest tests/auth/test_login.py

# Specific test
pytest tests/auth/test_login.py::test_login

# Match by keyword
pytest -k "login"

# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3
```

---

## API Endpoints Reference

### Authentication Endpoints

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/api/v1/auth/login` | POST | User login | `{username, password}` | `{accessToken, refreshToken}` |
| `/api/v1/auth/refresh` | POST | Refresh access token | `{refreshToken}` | `{accessToken, refreshToken}` |

### Data Endpoints (Template)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/data/create` | POST | Create data item |
| `/api/v1/data` | GET | List data items |
| `/api/v1/data/{id}` | GET | Get data item |
| `/api/v1/data/{id}` | PUT | Update data item |
| `/api/v1/data/{id}` | DELETE | Delete data item |

---

## Command Reference

### Test Execution

```bash
# Run all tests
pytest

# Run tests on specific environment
pytest --env dev
pytest --env qa
pytest --env prod

# Run specific test file
pytest tests/auth/test_login.py

# Run specific test function
pytest tests/auth/test_login.py::test_login

# Run tests matching pattern
pytest -k "login"

# Run with specific marker
pytest -m "order(1)"

# Run with detailed output
pytest -v -s

# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Show slowest tests
pytest --durations=10
```

### Report Generation

```bash
# HTML report
pytest --html=reports/report.html --self-contained-html

# Allure report (data)
pytest --alluredir=allure-results

# Allure report (clean old data)
pytest --alluredir=allure-results --clean-alluredir

# View Allure report
allure serve allure-results

# Allure report with custom port
allure serve allure-results --port 8080
```

### Debug Commands

```bash
# Collect only (list tests)
pytest --collect-only

# Debug mode (stop on failure)
pytest --pdb

# Debug on error
pytest --pdbcls=IPython.terminal.debugger:TerminalPdb

# Verbose logging
pytest --log-cli-level=DEBUG

# Capture output
pytest --capture=no

# Show print statements
pytest -s

# Test coverage
pytest --cov=core tests/
```

---

## FAQ

### Q: How do I run tests?

**A**: Use `pytest` to run all tests or `pytest tests/file.py` for specific file.

```bash
pytest                              # All tests
pytest --env qa                     # On QA
pytest tests/auth/test_login.py    # Specific file
```

### Q: How do I write a new test?

**A**: Create a test file in `tests/` directory starting with `test_` and use the `api_client` fixture.

```python
def test_example(api_client):
    response = api_client.get("/api/v1/data")
    assert response.status_code == 200
```

### Q: How does token refresh work?

**A**: When a request gets 401, the APIClient automatically uses the refresh token to get a new access token and retries the request.

```python
# Automatic - no code needed
response = api_client.get("/api/v1/data")  # Refreshes if needed
```

### Q: How do I configure a new environment?

**A**: Create a new YAML file in `config/` and use with `--env` flag.

```bash
# Create config/staging.yaml
pytest --env staging
```

### Q: What fixtures are available?

**A**: 
- `config` - Configuration
- `auth_tokens` - Login tokens
- `api_client` - API client
- `access_token` - Access token string
- `refresh_token` - Refresh token string

### Q: How do I generate reports?

**A**: Use `--html` or `--alluredir` flags.

```bash
pytest --html=reports/report.html
pytest --alluredir=allure-results
allure serve allure-results
```

### Q: How do I use fixtures?

**A**: Request them as function parameters.

```python
def test_example(api_client, config):
    response = api_client.get("/api/v1/data")
    assert response.status_code == 200
```

### Q: How do I parametrize tests?

**A**: Use `@pytest.mark.parametrize` decorator.

```python
@pytest.mark.parametrize("item_name", ["Item1", "Item2"])
def test_create_items(api_client, item_name):
    response = api_client.post(
        "/api/v1/data",
        json={"name": item_name}
    )
    assert response.status_code == 200
```

### Q: How do I handle test dependencies?

**A**: Use `@pytest.mark.order()` for test ordering.

```python
@pytest.mark.order(1)
def test_login_first(auth_tokens):
    assert auth_tokens["access_token"]

@pytest.mark.order(2)
def test_api_operations_second(api_client):
    response = api_client.post("/api/v1/data", json={})
    assert response.status_code == 200
```

### Q: How do I debug a failing test?

**A**: Use `-v -s` flags or `--pdb` for debugger.

```bash
pytest tests/file.py::test_name -v -s
pytest tests/file.py::test_name --pdb
pytest tests/file.py::test_name --log-cli-level=DEBUG
```

### Q: How do I validate responses?

**A**: Use schema validation or assertions.

```python
# Schema validation
from helpers.validators.schema_validator import validate_schema
validate_schema(response.json(), DATA_SCHEMA)

# Assertions
assert response.status_code == 200
assert "id" in response.json()
```

### Q: Where are my test results?

**A**: HTML reports in `reports/` and Allure data in `allure-results/`.

```bash
open reports/report.html                 # View HTML report
allure serve allure-results             # View Allure report
```

---

## Summary

This framework provides a comprehensive solution for API testing with:

✅ **Automatic Authentication** - Login and token management handled automatically  
✅ **Token Refresh** - Automatic token refresh on expiration  
✅ **Configuration Management** - YAML-based environment configuration  
✅ **Testing Features** - Parametrization, ordering, and fixtures  
✅ **Reporting** - HTML and Allure reports with trends  
✅ **Validation** - Schema validation for responses  
✅ **Organization** - Feature-based test structure  
✅ **Logging** - Complete request/response logging  

### Quick Reference

**Start Here**: Run `pytest --env dev` to execute tests

**Write Tests**: Use `api_client` fixture to make HTTP calls

**Configure**: Edit YAML files in `config/` directory

**Report**: Generate reports with `--html` or `--alluredir` flags

**Debug**: Use `-v -s --log-cli-level=DEBUG` for debugging

---

**Version**: 1.0.0  
**Last Updated**: March 17, 2026  

This is a universal, production-ready API testing framework documentation that can be used for any REST/HTTP API project.

