# Fixtures Reference

## Overview

Pytest fixtures are reusable functions that provide setup/teardown for tests. This guide covers all available fixtures in COMS Pytest.

---

## Table of Contents

1. [Built-in Fixtures](#built-in-fixtures)
2. [Creating Custom Fixtures](#creating-custom-fixtures)
3. [Fixture Scopes](#fixture-scopes)
4. [Fixture Parameters](#fixture-parameters)
5. [Best Practices](#best-practices)
6. [Examples](#examples)

---

## Built-in Fixtures

All fixtures are defined in `conftest.py` and available throughout the test suite.

### config

**Scope**: `session` (one per test session)

**Returns**: Dictionary containing environment configuration

**Usage**:
```python
def test_with_config(config):
    """Access environment configuration."""
    assert config["base_url"]
    assert config["credentials"]["email"]
```

**Available Properties**:
```python
config["base_url"]              # API base URL
config["login_endpoint"]        # Login endpoint
config["refresh_endpoint"]      # Token refresh endpoint
config["credentials"]["email"]  # User email
config["credentials"]["password"]  # User password
```

### auth_tokens

**Scope**: `session` (one per test session)

**Returns**: Dictionary with access_token and refresh_token

**Usage**:
```python
def test_with_tokens(auth_tokens):
    """Access authentication tokens."""
    access_token = auth_tokens["access_token"]
    refresh_token = auth_tokens["refresh_token"]
    assert access_token
    assert refresh_token
```

**Token Structure**:
```python
{
    "access_token": "eyJhbGciOiJIUzUxMiJ9...",
    "refresh_token": "eyJhbGciOiJIUzUxMiJ9..."
}
```

### api_client

**Scope**: `session` (one per test session)

**Returns**: Authenticated APIClient instance

**Usage**:
```python
def test_with_client(api_client):
    """Make authenticated API requests."""
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200
```

**Features**:
- ✅ Automatic token refresh on 401
- ✅ Request/response logging
- ✅ Authentication headers
- ✅ Fallback to login on refresh failure

### access_token

**Scope**: `session`

**Returns**: Access token string

**Usage**:
```python
def test_with_access_token(access_token):
    """Get access token directly."""
    assert access_token
    assert access_token.startswith("eyJ")  # JWT format
```

### refresh_token

**Scope**: `session`

**Returns**: Refresh token string

**Usage**:
```python
def test_with_refresh_token(refresh_token):
    """Get refresh token directly."""
    assert refresh_token
    assert refresh_token.startswith("eyJ")
```

---

## Creating Custom Fixtures

### Basic Fixture

```python
# conftest.py or test file

import pytest

@pytest.fixture
def sample_data():
    """Fixture providing sample data."""
    return {
        "name": "Test Organization",
        "email": "test@org.com"
    }

# Usage in test
def test_with_sample_data(sample_data):
    assert sample_data["name"] == "Test Organization"
```

### Fixture with Setup and Teardown

```python
@pytest.fixture
def created_organization(api_client):
    """Create organization and cleanup after test."""
    # Setup
    payload = {"name": "Test Org"}
    response = api_client.post("/api/v1/organizations", json=payload)
    org_id = response.json()["responseObject"]["organizationId"]
    
    yield org_id  # Provide to test
    
    # Teardown
    api_client.delete(f"/api/v1/organizations/{org_id}")

# Usage
def test_with_org(created_organization):
    """Test uses created org and cleanup happens automatically."""
    org_id = created_organization
    assert org_id
    # Test code here
    # Organization is automatically deleted after test
```

### Parametrized Fixtures

```python
@pytest.fixture(params=[
    {"name": "Org1"},
    {"name": "Org2"},
    {"name": "Org3"}
])
def organization_payloads(request):
    """Fixture providing multiple payloads."""
    return request.param

# Usage
def test_create_orgs(api_client, organization_payloads):
    """Test runs once for each payload."""
    response = api_client.post(
        "/api/v1/organizations",
        json=organization_payloads
    )
    assert response.status_code == 200
```

### Fixture Depending on Other Fixtures

```python
@pytest.fixture
def auth_headers(access_token):
    """Create auth headers using access token."""
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

# Usage
def test_with_headers(api_client, auth_headers):
    """Test using custom headers."""
    response = api_client.get(
        "/api/v1/organizations",
        headers=auth_headers
    )
    assert response.status_code == 200
```

---

## Fixture Scopes

### Function Scope (Default)

**Runs**: Once per test function

```python
@pytest.fixture(scope="function")
def fresh_data():
    """New data for each test."""
    return {"id": 1}

# Each test gets a fresh fixture instance
def test_1(fresh_data):
    assert fresh_data["id"] == 1

def test_2(fresh_data):
    assert fresh_data["id"] == 1  # Different instance
```

### Class Scope

**Runs**: Once per test class

```python
@pytest.fixture(scope="class")
def shared_org(api_client):
    """Org shared by all tests in class."""
    response = api_client.post("/api/v1/organizations", json={"name": "Test"})
    return response.json()["responseObject"]["organizationId"]

class TestOrganizations:
    def test_1(self, shared_org):
        assert shared_org
    
    def test_2(self, shared_org):
        assert shared_org  # Same instance as test_1
```

### Module Scope

**Runs**: Once per test module

```python
@pytest.fixture(scope="module")
def module_org(api_client):
    """Org shared by all tests in module."""
    response = api_client.post("/api/v1/organizations", json={"name": "Module Org"})
    return response.json()["responseObject"]["organizationId"]

# All tests in this module share the same org
```

### Session Scope

**Runs**: Once per test session

```python
@pytest.fixture(scope="session")
def session_client():
    """Client shared by all tests in session."""
    # Like api_client from conftest.py
    return create_client()

# All tests in entire session use same client
```

---

## Fixture Parameters

### Using request.param

```python
@pytest.fixture(params=[
    {"status": "active"},
    {"status": "inactive"}
])
def org_filters(request):
    """Parametrized fixture."""
    return request.param

def test_filters(api_client, org_filters):
    """Test runs for each parameter."""
    response = api_client.get(
        "/api/v1/organizations",
        params=org_filters
    )
    assert response.status_code == 200
```

### Using request.getfixturevalue()

```python
@pytest.fixture
def get_any_fixture(request):
    """Get any fixture dynamically."""
    def _get(fixture_name):
        return request.getfixturevalue(fixture_name)
    return _get

def test_dynamic(get_any_fixture):
    """Dynamically get fixtures."""
    config = get_any_fixture("config")
    api_client = get_any_fixture("api_client")
    assert config
    assert api_client
```

---

## Best Practices

### 1. Use Appropriate Scope

```python
# Good: Session scope for expensive operations
@pytest.fixture(scope="session")
def api_client():
    """Expensive to create, reuse across tests."""
    pass

# Good: Function scope for data that changes
@pytest.fixture(scope="function")
def sample_payload():
    """Create fresh data for each test."""
    return {"name": "test"}
```

### 2. Clear Fixture Names

```python
# Good: Descriptive names
@pytest.fixture
def created_organization(api_client):
    pass

@pytest.fixture
def valid_org_payload():
    pass

# Avoid: Vague names
@pytest.fixture
def data():
    pass

@pytest.fixture
def x():
    pass
```

### 3. Single Responsibility

```python
# Good: Fixture does one thing
@pytest.fixture
def organization_payload():
    """Provides valid organization payload."""
    return {"name": "Test Org"}

# Avoid: Fixture does multiple things
@pytest.fixture
def everything():
    """Create client, login, create org, get token..."""
    pass
```

### 4. Proper Cleanup

```python
# Good: Ensures cleanup happens
@pytest.fixture
def resource(api_client):
    # Setup
    response = api_client.post("/api/v1/resources", json={})
    resource_id = response.json()["responseObject"]["id"]
    
    yield resource_id  # Provide to test
    
    # Cleanup
    api_client.delete(f"/api/v1/resources/{resource_id}")

# Avoid: Cleanup not guaranteed
@pytest.fixture
def resource(api_client):
    response = api_client.post("/api/v1/resources", json={})
    return response.json()["responseObject"]["id"]
    # Cleanup never happens
```

### 5. Use request Object

```python
# Good: Use request for flexibility
@pytest.fixture
def fixture_info(request):
    """Get info about the requesting test."""
    test_name = request.node.name
    test_file = request.node.fspath
    return {"name": test_name, "file": test_file}

# Usage
def test_with_info(fixture_info):
    print(f"Running: {fixture_info['name']}")
```

### 6. Document Fixtures

```python
@pytest.fixture(scope="session")
def api_client(config, auth_tokens):
    """
    Provide authenticated API client.
    
    This fixture creates an APIClient instance that:
    - Automatically handles token refresh on 401
    - Logs all requests/responses
    - Falls back to login if refresh fails
    
    Scope: session - reused across all tests
    
    Returns:
        APIClient: Authenticated API client instance
    """
    def login_func():
        return login(...)
    
    return APIClient(...)
```

---

## Examples

### Example 1: Organization CRUD Fixtures

```python
# conftest.py or fixture file

import pytest

@pytest.fixture
def org_payload():
    """Valid organization payload."""
    return {
        "name": "Test Organization",
        "email": "org@test.com",
        "phone": "+1234567890"
    }

@pytest.fixture
def created_org(api_client, org_payload):
    """Create and cleanup organization."""
    response = api_client.post("/api/v1/organizations", json=org_payload)
    org = response.json()["responseObject"]
    
    yield org
    
    # Cleanup
    api_client.delete(f"/api/v1/organizations/{org['organizationId']}")

@pytest.fixture
def multiple_orgs(api_client):
    """Create multiple organizations."""
    orgs = []
    for i in range(3):
        payload = {"name": f"Org{i}"}
        response = api_client.post("/api/v1/organizations", json=payload)
        orgs.append(response.json()["responseObject"])
    
    yield orgs
    
    # Cleanup all
    for org in orgs:
        api_client.delete(f"/api/v1/organizations/{org['organizationId']}")

# Usage
def test_single_org(created_org):
    """Use single created org."""
    assert created_org["organizationId"]

def test_multiple_orgs(multiple_orgs):
    """Use multiple created orgs."""
    assert len(multiple_orgs) == 3
```

### Example 2: Data Fixtures

```python
@pytest.fixture
def valid_email():
    """Valid email address."""
    return "test@example.com"

@pytest.fixture
def invalid_emails():
    """Collection of invalid emails."""
    return [
        "invalid",
        "no@domain",
        "@example.com",
        "spaces in@email.com"
    ]

@pytest.fixture
def strong_password():
    """Valid password."""
    return "SecurePass123!@#"

@pytest.fixture
def weak_passwords():
    """Collection of weak passwords."""
    return [
        "123",
        "password",
        "pass",
        "12345678"
    ]

# Usage
def test_valid_email(api_client, valid_email):
    """Test with valid email."""
    response = api_client.post(
        "/api/v1/users",
        json={"email": valid_email}
    )
    assert response.status_code == 200

@pytest.mark.parametrize("email", [None])
def test_invalid_emails(api_client, invalid_emails):
    """Test with invalid emails."""
    for email in invalid_emails:
        response = api_client.post(
            "/api/v1/users",
            json={"email": email}
        )
        assert response.status_code == 400
```

### Example 3: Conditional Fixtures

```python
@pytest.fixture
def client_for_env(config, api_client, request):
    """Return appropriate client based on environment."""
    if "prod" in config["base_url"]:
        pytest.skip("Skipping on production")
    return api_client

def test_dev_only(client_for_env):
    """Test that skips on production."""
    response = client_for_env.get("/api/v1/debug")
    assert response.status_code == 200
```

### Example 4: Fixture with Configuration

```python
@pytest.fixture
def client_with_timeout(config):
    """Create client with custom timeout."""
    import requests
    session = requests.Session()
    session.timeout = config.get("timeout", 30)
    return session

def test_with_timeout(client_with_timeout):
    """Make request with custom timeout."""
    try:
        response = client_with_timeout.get(
            "https://api.example.com/slow-endpoint",
            timeout=client_with_timeout.timeout
        )
    except requests.Timeout:
        pytest.skip("Endpoint too slow")
```

---

## Fixture Execution Order

### Session-Level Fixtures

```python
# Execution order for session scope

@pytest.fixture(scope="session")
def first_fixture():
    print("Session setup")
    yield
    print("Session teardown")

@pytest.fixture(scope="session", autouse=True)
def always_runs_first(first_fixture):
    """Runs before first_fixture due to dependency."""
    pass
```

### Auto-Use Fixtures

```python
# Runs automatically without being requested

@pytest.fixture(autouse=True)
def auto_cleanup(api_client):
    """Cleanup after each test automatically."""
    yield
    # Cleanup code
    api_client.delete("/api/v1/temp")
```

---

## Common Patterns

### Pattern 1: Resource Management

```python
@pytest.fixture
def managed_resource(api_client):
    """Create and manage resource lifecycle."""
    # Create
    response = api_client.post("/api/v1/resources", json={})
    resource_id = response.json()["responseObject"]["id"]
    
    # Provide
    yield resource_id
    
    # Cleanup
    api_client.delete(f"/api/v1/resources/{resource_id}")
```

### Pattern 2: Context Manager

```python
from contextlib import contextmanager

@contextmanager
def temp_resource(api_client):
    """Create temporary resource."""
    response = api_client.post("/api/v1/resources", json={})
    resource_id = response.json()["responseObject"]["id"]
    
    try:
        yield resource_id
    finally:
        api_client.delete(f"/api/v1/resources/{resource_id}")

@pytest.fixture
def temp_org(api_client):
    """Fixture wrapper around context manager."""
    with temp_resource(api_client) as resource_id:
        yield resource_id
```

### Pattern 3: Factory Fixture

```python
@pytest.fixture
def org_factory(api_client):
    """Factory for creating organizations."""
    created_orgs = []
    
    def create(name="Test Org"):
        response = api_client.post(
            "/api/v1/organizations",
            json={"name": name}
        )
        org_id = response.json()["responseObject"]["organizationId"]
        created_orgs.append(org_id)
        return org_id
    
    yield create
    
    # Cleanup all created orgs
    for org_id in created_orgs:
        api_client.delete(f"/api/v1/organizations/{org_id}")

# Usage
def test_multiple_orgs(org_factory):
    """Create multiple orgs using factory."""
    org1 = org_factory("Org1")
    org2 = org_factory("Org2")
    assert org1
    assert org2
```

---

## Troubleshooting

### Issue: Fixture Not Running

**Problem**: Fixture setup code not executing

**Solution**:
```python
# Add autouse=True to run automatically
@pytest.fixture(autouse=True)
def my_fixture():
    print("This always runs")
    yield

# Or request it in test
def test_example(my_fixture):
    """Test requests fixture."""
    pass
```

### Issue: Scope Conflict

**Problem**: `ScopeMismatch` error

**Cause**: Function-scoped fixture depends on module-scoped fixture

**Solution**:
```python
# Change scope to match or lower
@pytest.fixture(scope="module")
def dependent_fixture(session_fixture):
    """Change to module or session scope."""
    pass
```

### Issue: Cleanup Not Running

**Problem**: Teardown code not executed

**Solution**:
```python
# Use yield, not return
@pytest.fixture
def my_fixture():
    setup()
    yield value    # Use yield for cleanup
    cleanup()
    
    # Not: return value (cleanup never runs)
```

---

## Related Documentation

- [Main README](../README.md)
- [API Client Guide](./API_CLIENT.md)
- [Testing Guide](./TESTING_GUIDE.md)
- [Configuration Guide](./CONFIGURATION.md)

