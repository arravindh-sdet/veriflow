# API Client Documentation

## Overview

The `APIClient` class is the core component for making HTTP requests with automatic token management, refresh handling, and logging.

## Class: APIClient

### Initialization

```python
APIClient(
    base_url: str,
    access_token: Optional[str] = None,
    refresh_token: Optional[str] = None,
    refresh_endpoint: str = "/api/v1/user/create/refreshToken",
    login_func: Optional[Callable[[], Dict[str, str]]] = None
)
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `base_url` | str | Yes | Base URL of the API (e.g., `https://api.example.com`) |
| `access_token` | str | No | Initial access token |
| `refresh_token` | str | No | Initial refresh token |
| `refresh_endpoint` | str | No | Endpoint for token refresh (default: `/api/v1/user/create/refreshToken`) |
| `login_func` | Callable | No | Function to call for login when refresh fails |

#### Example

```python
from core.api_client import APIClient
from core.auth import login

# Define login function
def my_login():
    return login(
        base_url="https://api.example.com",
        endpoint="/api/v1/user/login",
        username="user@example.com",
        password="password"
    )

# Create client
client = APIClient(
    base_url="https://api.example.com",
    access_token="initial_access_token",
    refresh_token="initial_refresh_token",
    refresh_endpoint="/api/v1/user/refreshToken",
    login_func=my_login
)
```

---

## Public Methods

### GET Request

```python
get(endpoint: str, params: dict = None, headers: dict = None) -> requests.Response
```

**Description**: Performs a GET request to the specified endpoint.

**Parameters**:
- `endpoint` (str): API endpoint (e.g., `/api/v1/organizations`)
- `params` (dict, optional): Query parameters
- `headers` (dict, optional): Custom headers

**Returns**: `requests.Response` object

**Example**:
```python
response = client.get("/api/v1/organizations")
assert response.status_code == 200

# With query parameters
response = client.get("/api/v1/organizations", params={"page": 1, "limit": 10})

# With custom headers
response = client.get("/api/v1/organizations", headers={"X-Custom": "value"})
```

---

### POST Request

```python
post(
    endpoint: str,
    json: dict = None,
    headers: dict = None,
    auth_required: bool = True
) -> requests.Response
```

**Description**: Performs a POST request with optional authentication.

**Parameters**:
- `endpoint` (str): API endpoint
- `json` (dict, optional): JSON payload
- `headers` (dict, optional): Custom headers
- `auth_required` (bool): Whether authentication is required (default: True)

**Returns**: `requests.Response` object

**Example**:
```python
payload = {
    "name": "New Organization",
    "email": "org@example.com"
}
response = client.post("/api/v1/organizations", json=payload)
assert response.status_code == 200

# Without authentication (for login)
response = client.post(
    "/api/v1/user/login",
    json={"username": "user", "password": "pass"},
    auth_required=False
)
```

---

### PUT Request

```python
put(
    endpoint: str,
    json: dict = None,
    headers: dict = None
) -> requests.Response
```

**Description**: Performs a PUT request to update a resource.

**Parameters**:
- `endpoint` (str): API endpoint
- `json` (dict, optional): JSON payload
- `headers` (dict, optional): Custom headers

**Returns**: `requests.Response` object

**Example**:
```python
updated_data = {"name": "Updated Organization"}
response = client.put("/api/v1/organizations/123", json=updated_data)
assert response.status_code == 200
```

---

### PATCH Request

```python
patch(
    endpoint: str,
    json: dict = None,
    headers: dict = None
) -> requests.Response
```

**Description**: Performs a PATCH request for partial updates.

**Parameters**:
- `endpoint` (str): API endpoint
- `json` (dict, optional): JSON payload
- `headers` (dict, optional): Custom headers

**Returns**: `requests.Response` object

**Example**:
```python
partial_update = {"name": "New Name"}
response = client.patch("/api/v1/organizations/123", json=partial_update)
assert response.status_code == 200
```

---

### DELETE Request

```python
delete(
    endpoint: str,
    headers: dict = None
) -> requests.Response
```

**Description**: Performs a DELETE request to remove a resource.

**Parameters**:
- `endpoint` (str): API endpoint
- `headers` (dict, optional): Custom headers

**Returns**: `requests.Response` object

**Example**:
```python
response = client.delete("/api/v1/organizations/123")
assert response.status_code == 204
```

---

## Private Methods (Internal)

### `_send_request()`

Internal method that handles all HTTP requests with automatic token refresh.

```python
_send_request(
    method: str,
    endpoint: str,
    auth_required: bool = True,
    retry: bool = True,
    **kwargs
) -> requests.Response
```

**Flow**:
1. Prepares headers with current access token
2. Makes the HTTP request
3. If 401 received and `auth_required=True` and `retry=True`:
   - Attempts token refresh
   - Falls back to login if refresh fails
   - Retries request with new token
4. Logs request and response
5. Returns response

---

### `_refresh_access_token()`

Refreshes the access token using the refresh token.

```python
_refresh_access_token() -> bool
```

**Returns**: `True` if refresh successful, `False` otherwise

**Process**:
1. Retrieves refresh token from token store
2. Makes POST request to refresh endpoint
3. Extracts new tokens from response
4. Updates token store
5. Returns success status

**Response Format Expected**:
```json
{
    "responseObject": {
        "accessToken": "new_access_token",
        "refreshToken": "new_refresh_token"
    }
}
```

---

### `_login()`

Attempts to log in using the login function.

```python
_login() -> bool
```

**Returns**: `True` if login successful, `False` otherwise

**Process**:
1. Checks if login function is defined
2. Calls login function
3. Updates token store with new tokens
4. Returns success status

---

### `_prepare_headers()`

Prepares headers with current access token.

```python
_prepare_headers(headers: dict = None) -> dict
```

**Returns**: Dictionary with headers including Authorization

**Process**:
1. Creates copy of provided headers (or empty dict)
2. Adds Bearer token if access token exists
3. Sets Content-Type to application/json if not set
4. Returns prepared headers

---

### `_log_request_response()`

Logs request and response to Allure for reporting.

```python
_log_request_response(
    method: str,
    url: str,
    headers: dict,
    payload: dict,
    response: requests.Response
)
```

**Attachments Created**:
- Request details (method, URL, headers, payload)
- Response data (status code, body)

---

## Token Management

### Token Storage

Tokens are stored in a dictionary:

```python
client.token_store = {
    "access_token": "current_access_token",
    "refresh_token": "current_refresh_token"
}
```

### Accessing Tokens

```python
current_access = client.token_store.get("access_token")
current_refresh = client.token_store.get("refresh_token")
```

### Updating Tokens

```python
client.token_store["access_token"] = "new_token"
client.token_store["refresh_token"] = "new_refresh"
```

---

## Token Refresh Flow

### Automatic Refresh on 401

```python
# Step 1: Request made
response = client.get("/api/v1/organizations")

# Step 2: If 401 received:
# - Refresh token automatically
# - Retry request with new token
# - If refresh fails, attempt login
# - Retry again

# Step 3: Return response (should be 200 if tokens refreshed)
```

### Manual Token Update

If you have new tokens from elsewhere:

```python
client.token_store["access_token"] = "new_access_token"
client.token_store["refresh_token"] = "new_refresh_token"
```

---

## Error Handling

### Request Failures

```python
try:
    response = client.get("/api/v1/organizations")
    response.raise_for_status()  # Raise exception for 4xx/5xx
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### Token Refresh Failures

```python
# If token refresh fails:
# 1. APIClient attempts login using login_func
# 2. If login also fails, request returns 401
# 3. Handle in your test

response = client.get("/api/v1/organizations")
if response.status_code == 401:
    # Authentication failed - tokens could not be refreshed
    print("Authentication failed")
```

---

## Configuration

### Using with Pytest Fixtures

```python
from conftest import api_client

def test_example(api_client):
    # api_client is already configured
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200
```

### Standalone Usage

```python
from core.api_client import APIClient
from core.auth import login
from core.config_loader import load_config

config = load_config("dev")

def login_func():
    return login(
        base_url=config["base_url"],
        endpoint=config["login_endpoint"],
        username=config["credentials"]["email"],
        password=config["credentials"]["password"]
    )

client = APIClient(
    base_url=config["base_url"],
    access_token=None,  # Will be set by login
    refresh_token=None,
    refresh_endpoint=config["refresh_endpoint"],
    login_func=login_func
)

# First login to get tokens
login_result = client._login()
if login_result:
    response = client.get("/api/v1/organizations")
```

---

## Best Practices

### 1. Always Use Fixtures

```python
# Good
def test_example(api_client):
    response = api_client.get("/api/v1/organizations")

# Avoid
def test_example():
    client = APIClient(...)  # Don't create new client each time
```

### 2. Check Response Status

```python
# Good
response = client.get("/api/v1/organizations")
assert response.status_code == 200
data = response.json()

# Avoid
data = client.get("/api/v1/organizations").json()  # No status check
```

### 3. Handle Different Response Types

```python
response = client.get("/api/v1/resource")
content_type = response.headers.get("Content-Type", "")

if "application/json" in content_type:
    data = response.json()
else:
    data = response.text
```

### 4. Use Custom Headers When Needed

```python
custom_headers = {
    "X-Custom-Header": "value",
    "X-Api-Version": "2"
}
response = client.post(
    "/api/v1/organizations",
    json={"name": "Org"},
    headers=custom_headers
)
```

### 5. Timeout Handling

```python
try:
    response = client.get("/api/v1/organizations")
except requests.exceptions.Timeout:
    # Server took too long to respond
    print("Request timed out")
```

---

## Debugging

### Enable Detailed Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Enable requests library logging
logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
```

### Check Token State

```python
# Print current tokens
print("Access Token:", client.token_store["access_token"])
print("Refresh Token:", client.token_store["refresh_token"])
```

### Verify Allure Logs

Allure automatically logs all requests/responses. Check `allure-results/` directory.

---

## Troubleshooting

### Issue: 401 Unauthorized Even After Refresh

**Causes**:
- Refresh token is expired
- Refresh endpoint URL is incorrect
- Server rejected refresh token

**Solution**:
```python
# Check if refresh endpoint is correct
print(client.refresh_endpoint)

# Verify token format
print(client.token_store)

# Check server response
response = client._refresh_access_token()
print(f"Refresh successful: {response}")
```

### Issue: Login Function Not Being Called

**Causes**:
- `login_func` not provided to APIClient
- Response is not 401

**Solution**:
```python
# Ensure login_func is provided
client = APIClient(
    base_url="...",
    login_func=my_login_function  # Must be provided
)
```

### Issue: Headers Not Being Set

**Causes**:
- Token is None
- Headers are immutable

**Solution**:
```python
# Ensure token exists
print(client.token_store["access_token"])

# Pass mutable headers dict
headers = {"X-Custom": "value"}
response = client.get("/api/v1/resource", headers=headers)
```

---

## Performance Tips

1. **Reuse Client**: Use pytest fixtures to reuse APIClient across tests
2. **Session Scope**: Configure `api_client` fixture with `scope="session"`
3. **Connection Pooling**: Requests library handles this automatically
4. **Batch Requests**: Make multiple requests in one test when logical

---

## Examples

### Complete Test Example

```python
import pytest
from core.api_client import APIClient

def test_organization_crud(api_client: APIClient):
    # Create
    create_payload = {"name": "Test Org", "email": "org@test.com"}
    create_response = api_client.post("/api/v1/organizations", json=create_payload)
    assert create_response.status_code == 200
    org_id = create_response.json()["responseObject"]["organizationId"]
    
    # Read
    get_response = api_client.get(f"/api/v1/organizations/{org_id}")
    assert get_response.status_code == 200
    
    # Update
    update_payload = {"name": "Updated Org"}
    update_response = api_client.put(
        f"/api/v1/organizations/{org_id}",
        json=update_payload
    )
    assert update_response.status_code == 200
    
    # Delete
    delete_response = api_client.delete(f"/api/v1/organizations/{org_id}")
    assert delete_response.status_code == 204
```

---

## Related Documentation

- [Main README](../README.md)
- [Testing Guide](./TESTING_GUIDE.md)
- [Configuration Guide](./CONFIGURATION.md)
- [Authentication](./AUTHENTICATION.md)

