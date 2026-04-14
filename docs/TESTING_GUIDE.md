# Testing Guide

## Overview

This guide provides comprehensive information on writing, organizing, and running tests in the COMS Pytest framework.

---

## Table of Contents

1. [Test Structure](#test-structure)
2. [Writing Tests](#writing-tests)
3. [Fixtures](#fixtures)
4. [Parametrized Tests](#parametrized-tests)
5. [Allure Integration](#allure-integration)
6. [Best Practices](#best-practices)
7. [Test Organization](#test-organization)
8. [Examples](#examples)

---

## Test Structure

### Basic Test File

```python
# tests/feature_name/test_something.py

import pytest
import allure
from core.api_client import APIClient

@allure.feature("Feature Name")
@allure.story("Story Name")
def test_basic_example(api_client):
    """Test description."""
    # Arrange
    payload = {"name": "test"}
    
    # Act
    response = api_client.post("/api/v1/resource", json=payload)
    
    # Assert
    assert response.status_code == 200
```

### Test Method Naming

| Pattern | Usage |
|---------|-------|
| `test_*` | Standard test function prefix |
| `*_test` | Alternative test function suffix |
| `Test*` | Test class names |
| `test_<feature>_<scenario>` | Recommended naming |

---

## Writing Tests

### AAA Pattern (Arrange-Act-Assert)

```python
def test_create_organization(api_client):
    # Arrange: Prepare test data
    payload = {
        "name": "Test Organization",
        "email": "test@org.com",
        "phone": "+1234567890"
    }
    
    # Act: Perform the action
    response = api_client.post("/api/v1/organizations", json=payload)
    
    # Assert: Verify results
    assert response.status_code == 200
    data = response.json()
    assert "organizationId" in data.get("responseObject", {})
```

### Response Assertions

```python
def test_response_validation(api_client):
    response = api_client.get("/api/v1/organizations")
    
    # Status code
    assert response.status_code == 200
    
    # Response type
    assert response.headers["Content-Type"] == "application/json"
    
    # Response content
    data = response.json()
    assert "responseObject" in data
    assert isinstance(data["responseObject"], list)
    
    # Specific fields
    for org in data["responseObject"]:
        assert "organizationId" in org
        assert "name" in org
```

### Exception Testing

```python
def test_invalid_request(api_client):
    payload = {"invalid_field": "value"}
    
    response = api_client.post("/api/v1/organizations", json=payload)
    
    # Check error status
    assert response.status_code == 400
    
    # Check error message
    data = response.json()
    assert "error" in data or "message" in data
```

---

## Fixtures

### Available Fixtures

From `conftest.py`:

| Fixture | Scope | Returns | Usage |
|---------|-------|---------|-------|
| `config` | session | Config dict | Access environment config |
| `auth_tokens` | session | Token dict | Get access/refresh tokens |
| `api_client` | session | APIClient | Make authenticated requests |
| `access_token` | session | str | Get access token string |
| `refresh_token` | session | str | Get refresh token string |

### Using Built-in Fixtures

```python
def test_with_config(config):
    """Access environment configuration."""
    base_url = config["base_url"]
    email = config["credentials"]["email"]
    assert base_url
    assert email

def test_with_api_client(api_client):
    """Make authenticated requests."""
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200

def test_with_tokens(access_token, refresh_token):
    """Access tokens directly."""
    assert access_token
    assert refresh_token
    assert len(access_token) > 0
```

### Creating Custom Fixtures

```python
# In conftest.py or test file

import pytest

@pytest.fixture
def sample_org_payload():
    """Fixture providing sample organization payload."""
    return {
        "name": "Test Organization",
        "email": "test@org.com",
        "phone": "+1234567890",
        "address": {
            "street": "123 Main St",
            "city": "Test City",
            "state": "TS",
            "zip": "12345",
            "country": "TC"
        }
    }

# Use in tests
def test_create_org(api_client, sample_org_payload):
    response = api_client.post("/api/v1/organizations", json=sample_org_payload)
    assert response.status_code == 200
```

### Fixture Scopes

```python
# Function scope (default) - new fixture per test
@pytest.fixture(scope="function")
def fresh_token(api_client):
    """New token for each test."""
    return api_client.token_store["access_token"]

# Module scope - one fixture per module
@pytest.fixture(scope="module")
def org_id(api_client):
    """Create org once per module."""
    response = api_client.post("/api/v1/organizations", json={"name": "Test"})
    return response.json()["responseObject"]["organizationId"]

# Session scope - one fixture for all tests
@pytest.fixture(scope="session")
def admin_client(config):
    """Admin client for entire session."""
    return create_admin_client(config)
```

### Fixture Teardown

```python
@pytest.fixture
def created_org(api_client):
    """Create org and clean up after test."""
    # Setup
    response = api_client.post("/api/v1/organizations", json={"name": "Test"})
    org_id = response.json()["responseObject"]["organizationId"]
    
    yield org_id  # Provide to test
    
    # Teardown
    api_client.delete(f"/api/v1/organizations/{org_id}")
```

---

## Parametrized Tests

### Basic Parametrization

```python
import pytest

@pytest.mark.parametrize(
    "name,email",
    [
        ("Org1", "org1@test.com"),
        ("Org2", "org2@test.com"),
        ("Org3", "org3@test.com"),
    ]
)
def test_create_multiple_orgs(api_client, name, email):
    payload = {"name": name, "email": email}
    response = api_client.post("/api/v1/organizations", json=payload)
    assert response.status_code == 200
```

### Parametrization with Case Names

```python
@pytest.mark.parametrize(
    "case_name,payload,expected_status",
    [
        ("valid_data", {"name": "Valid Org"}, 200),
        ("missing_name", {"email": "org@test.com"}, 400),
        ("invalid_email", {"name": "Org", "email": "invalid"}, 400),
    ]
)
def test_org_validation(api_client, case_name, payload, expected_status):
    response = api_client.post("/api/v1/organizations", json=payload)
    assert response.status_code == expected_status
```

### Dynamic Parametrization

```python
from utilities.payloads.organization.organization_payloads import OrganizationPayload

@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.missing_root_fields())
)
def test_missing_fields(api_client, case_name, payload):
    response = api_client.post("/api/v1/organizations", json=payload)
    assert response.status_code == 400
```

---

## Allure Integration

### Adding Allure Decorators

```python
import allure

@allure.feature("Organization Management")
@allure.story("Create Organization")
@allure.title("Create a new organization with valid data")
@allure.description("Verify that a new organization can be created with valid data")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_organization(api_client):
    response = api_client.post("/api/v1/organizations", json={"name": "Test"})
    assert response.status_code == 200
```

### Allure Severity Levels

```python
import allure

@allure.severity(allure.severity_level.BLOCKER)      # Entire system down
def test_critical_feature():
    pass

@allure.severity(allure.severity_level.CRITICAL)     # Major functionality broken
def test_major_feature():
    pass

@allure.severity(allure.severity_level.NORMAL)       # Standard test
def test_normal_feature():
    pass

@allure.severity(allure.severity_level.MINOR)        # Minor issue
def test_minor_feature():
    pass

@allure.severity(allure.severity_level.TRIVIAL)      # Cosmetic issue
def test_trivial_feature():
    pass
```

### Adding Steps to Tests

```python
import allure

def test_organization_workflow(api_client):
    with allure.step("Create organization"):
        response = api_client.post("/api/v1/organizations", json={"name": "Test"})
        assert response.status_code == 200
        org_id = response.json()["responseObject"]["organizationId"]
    
    with allure.step("Retrieve organization"):
        response = api_client.get(f"/api/v1/organizations/{org_id}")
        assert response.status_code == 200
    
    with allure.step("Update organization"):
        response = api_client.put(
            f"/api/v1/organizations/{org_id}",
            json={"name": "Updated"}
        )
        assert response.status_code == 200
    
    with allure.step("Delete organization"):
        response = api_client.delete(f"/api/v1/organizations/{org_id}")
        assert response.status_code == 204
```

### Attaching Evidence

```python
import allure
import json

def test_with_attachments(api_client):
    response = api_client.get("/api/v1/organizations")
    
    # Attach JSON response
    allure.attach(
        json.dumps(response.json(), indent=2),
        name="API Response",
        attachment_type=allure.attachment_type.JSON
    )
    
    # Attach text
    allure.attach(
        f"Status Code: {response.status_code}\nHeaders: {dict(response.headers)}",
        name="Response Details",
        attachment_type=allure.attachment_type.TEXT
    )
```

### Test Links

```python
import allure

@allure.link("https://jira.example.com/browse/TEST-123", name="Jira Issue")
@allure.link("https://example.com/test-cases/123", name="Test Case")
def test_with_links(api_client):
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200
```

---

## Test Ordering

### Using pytest-order

```python
import pytest

@pytest.mark.order(1)
def test_login_first(auth_tokens):
    """This test runs first."""
    assert auth_tokens["access_token"]

@pytest.mark.order(2)
def test_create_org_second(api_client):
    """This test runs second."""
    response = api_client.post("/api/v1/organizations", json={"name": "Test"})
    assert response.status_code == 200

@pytest.mark.order(3)
def test_verify_org_third(api_client):
    """This test runs third."""
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200
```

---

## Best Practices

### 1. Test Independence

```python
# Good: Each test is independent
def test_create_org_1(api_client):
    response = api_client.post("/api/v1/organizations", json={"name": "Test1"})
    assert response.status_code == 200

def test_create_org_2(api_client):
    response = api_client.post("/api/v1/organizations", json={"name": "Test2"})
    assert response.status_code == 200

# Avoid: Tests that depend on each other
def test_create_org_dependent():
    # Test 1
    response = api_client.post(...)
    
    # Test 2 (depends on Test 1 output)
    response = api_client.get(...)
```

### 2. Clear Assertions

```python
# Good: Specific assertions with context
def test_org_creation(api_client):
    response = api_client.post("/api/v1/organizations", json={"name": "Test"})
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "organizationId" in response.json()["responseObject"]

# Avoid: Vague assertions
def test_org_creation(api_client):
    response = api_client.post("/api/v1/organizations", json={"name": "Test"})
    assert response  # What does this test?
```

### 3. Use Descriptive Names

```python
# Good: Descriptive test names
def test_create_org_with_valid_email():
    pass

def test_create_org_with_missing_name():
    pass

# Avoid: Vague names
def test_org():
    pass

def test_1():
    pass
```

### 4. Data-Driven Testing

```python
# Good: Use fixtures and parametrization
@pytest.mark.parametrize("org_name", ["Org1", "Org2", "Org3"])
def test_create_orgs(api_client, org_name):
    response = api_client.post(
        "/api/v1/organizations",
        json={"name": org_name}
    )
    assert response.status_code == 200

# Avoid: Hardcoded test data
def test_create_org_1(api_client):
    response = api_client.post(...)
    assert response.status_code == 200

def test_create_org_2(api_client):
    response = api_client.post(...)
    assert response.status_code == 200
```

### 5. Validation Helpers

```python
from helpers.validators.schema_validator import validate_schema
from utilities.organization_schema import ORGANIZATION_SCHEMA

def test_org_response_schema(api_client):
    response = api_client.get("/api/v1/organizations/123")
    
    # Validate against schema
    validate_schema(response.json(), ORGANIZATION_SCHEMA)
```

### 6. Use Response Wrappers

```python
from helpers.wrappers.organization_wrapper import ResponseWrapper

def test_org_wrapper(api_client):
    response = api_client.get("/api/v1/organizations/123")
    
    # Easy access to nested fields
    wrapped = ResponseWrapper(response.json())
    org_id = wrapped.responseObject.organizationId
    org_name = wrapped.responseObject.name
    
    assert org_id
    assert org_name
```

---

## Test Organization

### Recommended Structure

```
tests/
├── auth/
│   ├── test_login.py              # Login tests
│   ├── test_login_negative.py     # Negative login tests
│   └── __init__.py
├── organizations/
│   ├── test_organization_crud.py  # CRUD operations
│   ├── test_org_validation.py     # Field validation
│   ├── test_org_pagination.py     # Pagination tests
│   └── __init__.py
├── users/
│   ├── test_user_management.py
│   └── __init__.py
└── __init__.py
```

### Test File Organization

```python
# tests/organizations/test_organization.py

import pytest
import allure
from utilities.payloads.organization.organization_payloads import OrganizationPayload
from helpers.validators.schema_validator import validate_schema

class TestOrganizationCreate:
    """Tests for organization creation."""
    
    @pytest.mark.order(1)
    def test_create_valid_org(self, api_client):
        """Create org with valid data."""
        response = api_client.post(
            "/api/v1/organizations",
            json=OrganizationPayload.valid()
        )
        assert response.status_code == 200
    
    @pytest.mark.parametrize("payload", OrganizationPayload.invalid())
    def test_create_invalid_org(self, api_client, payload):
        """Create org with invalid data."""
        response = api_client.post("/api/v1/organizations", json=payload)
        assert response.status_code == 400

class TestOrganizationRead:
    """Tests for reading organization data."""
    
    def test_get_organization(self, api_client):
        """Retrieve organization by ID."""
        response = api_client.get("/api/v1/organizations/123")
        assert response.status_code == 200

class TestOrganizationUpdate:
    """Tests for updating organization data."""
    
    def test_update_organization(self, api_client):
        """Update organization details."""
        response = api_client.put(
            "/api/v1/organizations/123",
            json={"name": "Updated"}
        )
        assert response.status_code == 200
```

---

## Examples

### Complete Test Suite Example

```python
# tests/organizations/test_organization_complete.py

import pytest
import allure
import json
from core.api_client import APIClient
from utilities.payloads.organization.organization_payloads import OrganizationPayload
from utilities.organization_schema import ORGANIZATION_SCHEMA
from helpers.validators.schema_validator import validate_schema
from helpers.wrappers.organization_wrapper import ResponseWrapper

@allure.feature("Organization Management")
class TestOrganizations:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        """Setup before each test."""
        self.api_client = api_client
        self.org_id = None
    
    def teardown_method(self):
        """Cleanup after each test."""
        if self.org_id:
            self.api_client.delete(f"/api/v1/organizations/{self.org_id}")
    
    @allure.story("Create Organization")
    @allure.title("Create organization with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_organization(self):
        """Create a new organization."""
        with allure.step("Prepare payload"):
            payload = OrganizationPayload.valid()
        
        with allure.step("Create organization"):
            response = self.api_client.post(
                "/api/v1/organizations",
                json=payload
            )
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            data = response.json()
            assert "responseObject" in data
            self.org_id = data["responseObject"]["organizationId"]
        
        with allure.step("Validate schema"):
            validate_schema(data, ORGANIZATION_SCHEMA)
    
    @allure.story("Read Organization")
    @pytest.mark.order(2)
    def test_get_organization(self):
        """Retrieve organization details."""
        # First create an org
        create_response = self.api_client.post(
            "/api/v1/organizations",
            json=OrganizationPayload.valid()
        )
        self.org_id = create_response.json()["responseObject"]["organizationId"]
        
        # Then retrieve it
        response = self.api_client.get(f"/api/v1/organizations/{self.org_id}")
        
        assert response.status_code == 200
        wrapped = ResponseWrapper(response.json())
        assert wrapped.responseObject.organizationId == self.org_id
    
    @allure.story("Update Organization")
    @pytest.mark.parametrize(
        "update_data",
        [
            {"name": "Updated Name"},
            {"phone": "+1987654321"},
        ]
    )
    def test_update_organization(self, update_data):
        """Update organization details."""
        # Create org
        create_response = self.api_client.post(
            "/api/v1/organizations",
            json=OrganizationPayload.valid()
        )
        self.org_id = create_response.json()["responseObject"]["organizationId"]
        
        # Update it
        response = self.api_client.put(
            f"/api/v1/organizations/{self.org_id}",
            json=update_data
        )
        
        assert response.status_code == 200
    
    @allure.story("Delete Organization")
    def test_delete_organization(self):
        """Delete an organization."""
        # Create org
        create_response = self.api_client.post(
            "/api/v1/organizations",
            json=OrganizationPayload.valid()
        )
        org_id = create_response.json()["responseObject"]["organizationId"]
        
        # Delete it
        response = self.api_client.delete(f"/api/v1/organizations/{org_id}")
        
        assert response.status_code == 204
        self.org_id = None  # Don't try to delete in teardown
    
    @allure.story("Validation")
    @pytest.mark.parametrize(
        "case_name,payload",
        list(OrganizationPayload.missing_root_fields())
    )
    def test_missing_fields_validation(self, case_name, payload):
        """Verify validation of missing required fields."""
        response = self.api_client.post(
            "/api/v1/organizations",
            json=payload
        )
        
        assert response.status_code == 400
```

---

## Running Tests

### Command Examples

```bash
# Run all tests
pytest

# Run specific file
pytest tests/organizations/test_organization.py

# Run specific test
pytest tests/organizations/test_organization.py::test_create_org

# Run with pattern
pytest tests/ -k "create"

# Run with markers
pytest -m "order(1)"

# Run with coverage
pytest --cov=core tests/

# Generate reports
pytest --html=reports/report.html --alluredir=allure-results

# Verbose output
pytest -v -s
```

---

## Debugging Tests

### Print Debug Information

```python
def test_debug_example(api_client):
    response = api_client.get("/api/v1/organizations")
    
    # Print response
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Body: {response.json()}")
    
    assert response.status_code == 200
```

### Run with verbose logging

```bash
pytest -v -s --log-cli-level=DEBUG
```

### Breakpoint Debugging

```python
def test_with_breakpoint(api_client):
    response = api_client.get("/api/v1/organizations")
    breakpoint()  # Pause here for inspection
    assert response.status_code == 200
```

---

## Related Documentation

- [Main README](../README.md)
- [API Client Guide](./API_CLIENT.md)
- [Configuration Guide](./CONFIGURATION.md)
- [Fixtures Reference](./FIXTURES.md)

