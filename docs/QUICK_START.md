# Quick Start Guide

## 5-Minute Setup

Get COMS Pytest up and running in minutes!

---

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd COMS_Pytest
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
pytest --version
```

---

## Configuration

### 1. Set Up Environment Config

The project includes pre-configured environments. Configuration files are in `config/` directory:

- `config/dev.yaml` - Development environment (default)
- `config/qa.yaml` - QA environment
- `config/prod.yaml` - Production environment

### 2. Update Credentials (if needed)

Keep `config/dev.yaml` as the public-safe template and add your real credentials in `config/dev.local.yaml`:

```yaml
base_url: "https://your-api-url.com"
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  email: "your-email@example.com"
  password: "your-password"
```

---

## Running Your First Test

### Basic Test Run

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with logs
pytest -s
```

### Run Specific Tests

```bash
# Run specific test file
pytest tests/auth/test_login.py

# Run specific test function
pytest tests/auth/test_login.py::test_login

# Run tests matching pattern
pytest -k "login"
```

### Run with Specific Environment

```bash
# Development (default)
pytest --env dev

# QA environment
pytest --env qa

# Production environment
pytest --env prod
```

---

## Generate Reports

### HTML Report

```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Report will be at: reports/report.html
```

### Allure Report

```bash
# Generate Allure report
pytest --alluredir=allure-results

# View in browser
allure serve allure-results
```

---

## Test Structure Overview

### Project Layout

```
tests/
├── auth/                           # Authentication tests
│   ├── test_login.py              # Login functionality
│   ├── test_login_negative.py     # Negative test cases
│   └── __init__.py
├── organisation/                   # Organization API tests
│   ├── test_organization.py       # CRUD operations
│   ├── test_org_pagination.py     # Pagination tests
│   └── __init__.py
└── __init__.py
```

### Sample Test

```python
# tests/auth/test_login.py
import pytest

@pytest.mark.order(1)
def test_login(auth_tokens):
    """Test user login."""
    assert "access_token" in auth_tokens
    assert "refresh_token" in auth_tokens
    print("✅ Login successful")
```

---

## Common Commands

### Test Execution

```bash
# All tests
pytest

# Verbose with output
pytest -v -s

# Stop on first failure
pytest -x

# Generate all reports
pytest -v -s --html=reports/report.html --alluredir=allure-results

# Run specific environment
pytest --env qa -v
```

### Test Organization

```bash
# List all tests
pytest --collect-only

# Run tests by marker
pytest -m "order(1)"

# Run tests by keyword
pytest -k "organization"
```

---

## Using API Client in Tests

### Basic Usage

```python
def test_create_organization(api_client):
    """Create new organization."""
    payload = {"name": "My Organization"}
    
    response = api_client.post(
        "/api/v1/organizations",
        json=payload
    )
    
    assert response.status_code == 200
    print("✅ Organization created")
```

### With Validation

```python
def test_org_with_schema(api_client):
    """Create and validate organization."""
    response = api_client.get("/api/v1/organizations/123")
    
    assert response.status_code == 200
    
    from helpers.validators.schema_validator import validate_schema
    from utilities.organization_schema import ORGANIZATION_SCHEMA
    
    validate_schema(response.json(), ORGANIZATION_SCHEMA)
    print("✅ Schema validation passed")
```

### With Allure Reporting

```python
import allure

@allure.feature("Organization")
@allure.story("Create")
def test_create_org(api_client):
    """Create organization with Allure reporting."""
    with allure.step("Prepare payload"):
        payload = {"name": "Test Org"}
    
    with allure.step("Send request"):
        response = api_client.post("/api/v1/organizations", json=payload)
    
    with allure.step("Verify response"):
        assert response.status_code == 200
```

---

## Token Management

### Automatic Token Refresh

The API client automatically handles token refresh:

```python
def test_with_auto_refresh(api_client):
    """Token refresh happens automatically on 401."""
    # If token expires during request, it's automatically refreshed
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200
    print("✅ Request succeeded (token refreshed if needed)")
```

### Manual Token Access

```python
def test_with_tokens(access_token, refresh_token):
    """Access tokens directly."""
    assert access_token
    assert refresh_token
    print(f"Access Token: {access_token[:20]}...")
```

---

## Fixtures - Reusable Test Setup

### Available Fixtures

```python
# Configuration
def test_with_config(config):
    """Access environment configuration."""
    base_url = config["base_url"]
    email = config["credentials"]["email"]

# Tokens
def test_with_tokens(auth_tokens):
    """Access authentication tokens."""
    access_token = auth_tokens["access_token"]
    refresh_token = auth_tokens["refresh_token"]

# API Client
def test_with_client(api_client):
    """Make authenticated API requests."""
    response = api_client.get("/api/v1/organizations")
```

### Creating Custom Fixtures

```python
# In conftest.py or test file

@pytest.fixture
def sample_org_payload():
    """Custom fixture providing test data."""
    return {"name": "Test Organization"}

# Use in test
def test_with_custom_fixture(api_client, sample_org_payload):
    response = api_client.post("/api/v1/organizations", json=sample_org_payload)
    assert response.status_code == 200
```

---

## Parametrized Tests

### Test Multiple Cases

```python
@pytest.mark.parametrize(
    "org_name",
    ["Org1", "Org2", "Org3"]
)
def test_create_multiple_orgs(api_client, org_name):
    """Test creates organization for each name."""
    response = api_client.post(
        "/api/v1/organizations",
        json={"name": org_name}
    )
    assert response.status_code == 200
```

---

## Troubleshooting

### Tests Not Running

**Problem**: No tests collected

**Solution**:
```bash
# Check pytest found tests
pytest --collect-only

# Run from project root
cd /path/to/COMS_Pytest

# Check file names start with test_
ls tests/
```

### Config Not Found

**Problem**: `FileNotFoundError: Config file not found`

**Solution**:
```bash
# Check config files exist
ls config/

# Run from project root directory
cd /path/to/COMS_Pytest

# Verify environment name
pytest --env dev
```

### Token Issues

**Problem**: Tests fail with 401 Unauthorized

**Solution**:
```bash
# Verify credentials in config/dev.yaml
# Update with valid credentials

# Check if tokens are being generated
pytest -s -v tests/auth/test_login.py
```

### Dependencies Missing

**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
# Reinstall requirements
pip install -r requirements.txt

# Verify installation
pip list | grep pytest
```

---

## Next Steps

### 1. Read Full Documentation

- **[Main README](../README.md)** - Complete project overview
- **[Testing Guide](TESTING_GUIDE.md)** - How to write tests
- **[API Client Guide](API_CLIENT.md)** - API client details
- **[Configuration Guide](CONFIGURATION.md)** - Setup configuration
- **[Fixtures Guide](FIXTURES.md)** - Using fixtures

### 2. Explore Test Examples

- Check `tests/auth/test_login.py` for basic examples
- Check `tests/organisation/test_organization.py` for complex examples

### 3. Write Your First Test

```python
# tests/my_first_test.py

import pytest

def test_hello_world(api_client):
    """Your first test."""
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200
    print("✅ Test passed!")
```

Run it:
```bash
pytest tests/my_first_test.py -v -s
```

### 4. Generate Reports

```bash
# Generate and view Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Quick Reference

### Commands

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -s` | Show print statements |
| `pytest tests/auth/test_login.py` | Run specific file |
| `pytest -k "login"` | Run tests matching pattern |
| `pytest --env qa` | Run on QA environment |
| `pytest --collect-only` | List all tests |
| `pytest --html=reports/report.html` | Generate HTML report |
| `allure serve allure-results` | View Allure report |

### Code Templates

**Simple Test**
```python
def test_example(api_client):
    response = api_client.get("/api/v1/endpoint")
    assert response.status_code == 200
```

**Parametrized Test**
```python
@pytest.mark.parametrize("value", [1, 2, 3])
def test_example(api_client, value):
    response = api_client.get(f"/api/v1/endpoint/{value}")
    assert response.status_code == 200
```

**With Allure**
```python
@allure.feature("Feature")
@allure.story("Story")
def test_example(api_client):
    response = api_client.get("/api/v1/endpoint")
    assert response.status_code == 200
```

### Fixtures

```python
# Use built-in fixtures
def test_with_client(api_client):
    pass

def test_with_config(config):
    pass

def test_with_tokens(auth_tokens):
    pass

# Create custom fixture
@pytest.fixture
def my_data():
    return {"key": "value"}
```

---

## Getting Help

### Check Documentation

1. **[Main README](../README.md)** - Overview and features
2. **[API Client](API_CLIENT.md)** - Making requests
3. **[Testing Guide](TESTING_GUIDE.md)** - Writing tests
4. **[Configuration](CONFIGURATION.md)** - Setting up environments
5. **[Fixtures](FIXTURES.md)** - Using fixtures

### Test Examples

- Check `tests/auth/test_login.py` for simple examples
- Check `tests/organisation/test_organization.py` for complex examples

### Debug Tests

```bash
# Verbose output
pytest -vvv

# Show print statements
pytest -s

# Debug on failure
pytest --pdb

# Log output
pytest --log-cli-level=DEBUG
```

---

## Summary

You're now ready to:
- ✅ Run tests
- ✅ Create new tests
- ✅ Use API client
- ✅ Generate reports
- ✅ Manage tokens
- ✅ Use fixtures

Happy testing! 🚀
