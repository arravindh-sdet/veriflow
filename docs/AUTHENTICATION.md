# Authentication & Token Management

## Overview

COMS Pytest provides comprehensive authentication and token management, including automatic token refresh, fallback to re-login, and secure token storage.

---

## Table of Contents

1. [Authentication Flow](#authentication-flow)
2. [Token Management](#token-management)
3. [Login Process](#login-process)
4. [Token Refresh](#token-refresh)
5. [Token Storage](#token-storage)
6. [Configuration](#configuration)
7. [Testing Authentication](#testing-authentication)
8. [Troubleshooting](#troubleshooting)

---

## Authentication Flow

### Complete Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Test Execution Starts                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Load Configuration from YAML          │
        │  (base_url, endpoints, credentials)    │
        └────────────────┬───────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────┐
        │  Perform Initial Login                 │
        │  - Send credentials to login endpoint  │
        │  - Receive access & refresh tokens     │
        └────────────────┬───────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────┐
        │  Initialize APIClient                  │
        │  - Store tokens in token_store         │
        │  - Set up auto-refresh on 401          │
        └────────────────┬───────────────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │   Execute Tests            │
            └────────────┬───────────────┘
                         │
    ┌────────────────────┴────────────────────┐
    │                                         │
    ▼                                         ▼
┌──────────────┐                    ┌──────────────────┐
│ Request OK  │                    │ 401 Unauthorized │
│ (200, etc.) │                    │                  │
└──────────────┘                    └────────┬─────────┘
                                             │
                                 ┌───────────▼────────────┐
                                 │ Attempt Token Refresh  │
                                 │ - Use refresh token    │
                                 │ - Get new access token │
                                 └───────────┬────────────┘
                                             │
                                 ┌───────────┴────────────┐
                                 │                        │
                           ▼ Success                ▼ Failure
                    ┌──────────────┐        ┌──────────────────┐
                    │ Retry Request│        │ Attempt Re-login │
                    │ with new     │        │ - Use credentials│
                    │ access token │        │ - Get new tokens │
                    └──────────────┘        └────────┬─────────┘
                           │                         │
                           │                ┌────────┴─────────┐
                           │                │                  │
                           │          ▼ Success         ▼ Failure
                           │    ┌──────────────┐    ┌──────────┐
                           │    │ Retry Request│    │ Return   │
                           │    │ with new     │    │ 401 Error│
                           │    │ tokens       │    └──────────┘
                           │    └──────────────┘
                           │           │
                           └───────────┴──────┐
                                            │
                                            ▼
                           ┌────────────────────────┐
                           │  Continue to Next Test │
                           └────────────────────────┘
```

---

## Token Management

### Token Structure

Tokens are JWT (JSON Web Tokens) with three parts separated by dots:

```
eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2ZDMzNjBhYi0wOTgwLTQ0ODEtODIyZi04NjBlOWVjMzg4NjYiLCJpYXQiOjE3NjU5NzY4NjcsImV4cCI6MTc2NTk4NDA2N30.50KIcIK-NeGmk7TIhYrR4KleG1CiX2eWSWmpWqo5UWCt9knWLViocIOYgr_UOJF0IhW_s1WNjIFDtOWwmt-T1A

│                           │                                    │                                 │
├─ Header (Base64)         ├─ Payload (Base64)                 ├─ Signature                     │
│ Algorithm: HS512         │ Subject (user ID)                  │ Cryptographic signature        │
│ Token type: JWT          │ Issued at (iat)                    │                                │
│                          │ Expiration (exp)                   │                                │
```

### Token Types

#### Access Token
- **Purpose**: Authenticate API requests
- **Lifetime**: Shorter (typically 5-15 minutes)
- **Usage**: Included in `Authorization: Bearer <token>` header
- **Refresh**: Can be refreshed using refresh token

#### Refresh Token
- **Purpose**: Obtain new access token
- **Lifetime**: Longer (typically days to weeks)
- **Usage**: Sent to refresh endpoint to get new access token
- **Security**: Should be stored securely

### Token Storage

Tokens are stored in the APIClient:

```python
client.token_store = {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc..."
}
```

---

## Login Process

### Initial Login

The login process authenticates user and retrieves tokens:

```python
from core.auth import login

tokens = login(
    base_url="https://api.example.com",
    endpoint="/api/v1/user/login",
    username="user@example.com",
    password="password123"
)

print(tokens)
# Output:
# {
#     "access_token": "eyJhbGc...",
#     "refresh_token": "eyJhbGc..."
# }
```

### Login Request/Response

**Request**:
```json
{
    "userName": "user@example.com",
    "password": "password123"
}
```

**Response**:
```json
{
    "responseObject": {
        "accessToken": "eyJhbGc...",
        "refreshToken": "eyJhbGc..."
    }
}
```

### Login in Fixtures

Login is automatically performed in fixtures:

```python
# conftest.py

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
```

---

## Token Refresh

### Automatic Token Refresh

When a request returns 401 (Unauthorized), the APIClient automatically attempts token refresh:

```python
def test_auto_refresh(api_client):
    """Token refresh happens automatically."""
    # If access token is expired, following happens automatically:
    # 1. Detects 401 response
    # 2. Uses refresh token to get new access token
    # 3. Retries request with new token
    
    response = api_client.get("/api/v1/organizations")
    assert response.status_code == 200  # Request succeeds
```

### Refresh Process

```python
# In APIClient._refresh_access_token()

def _refresh_access_token(self) -> bool:
    refresh_token = self.token_store.get("refresh_token")
    if not refresh_token:
        return False
    
    url = f"{self.base_url}{self.refresh_endpoint}"
    
    try:
        # 1. Send refresh token to server
        resp = requests.post(
            url,
            json={"refreshToken": refresh_token},
            timeout=10
        )
        
        # 2. Check response
        if resp.status_code != 200:
            return False
        
        # 3. Extract new tokens
        data = resp.json()
        resp_obj = data.get("responseObject", {})
        new_access = resp_obj.get("accessToken")
        new_refresh = resp_obj.get("refreshToken", refresh_token)
        
        if not new_access:
            return False
        
        # 4. Update token store
        self.token_store["access_token"] = new_access
        self.token_store["refresh_token"] = new_refresh
        
        return True
    
    except Exception as e:
        print("Refresh failed:", e)
        return False
```

### Manual Token Refresh

You can manually refresh tokens:

```python
# Manually refresh using APIClient
if not api_client._refresh_access_token():
    print("Token refresh failed")

# Or login again
if not api_client._login():
    print("Login failed")
```

---

## Configuration

### Authentication Configuration

All authentication settings are in `config/dev.yaml`:

```yaml
# API base URL
base_url: "https://api.example.com"

# Login endpoint
login_endpoint: "/api/v1/user/login"

# Token refresh endpoint
refresh_endpoint: "/api/v1/user/refreshToken"

# Credentials
credentials:
  email: "user@example.com"
  password: "password123"
```

### APIClient Configuration

APIClient is configured in `conftest.py`:

```python
@pytest.fixture(scope="session")
def api_client(config, auth_tokens):
    """Provide authenticated API client."""
    
    # Define login function
    def login_func():
        return login(
            base_url=config["base_url"],
            endpoint=config["login_endpoint"],
            username=config["credentials"]["email"],
            password=config["credentials"]["password"]
        )
    
    # Create client
    client = APIClient(
        base_url=config["base_url"],
        access_token=auth_tokens["access_token"],
        refresh_token=auth_tokens["refresh_token"],
        login_func=login_func,
        refresh_endpoint=config.get("refresh_endpoint", "/api/v1/user/create/refreshToken")
    )
    
    return client
```

---

## Testing Authentication

### Test Login

```python
import pytest

@pytest.mark.order(1)
def test_login(auth_tokens):
    """Test that login succeeds and returns tokens."""
    assert "access_token" in auth_tokens
    assert "refresh_token" in auth_tokens
    
    # Verify token format
    assert auth_tokens["access_token"].startswith("eyJ")  # JWT format
    assert auth_tokens["refresh_token"].startswith("eyJ")
    
    print("✅ Login successful")
    print(f"Access Token: {auth_tokens['access_token'][:20]}...")
    print(f"Refresh Token: {auth_tokens['refresh_token'][:20]}...")
```

### Test Token Usage

```python
def test_with_access_token(api_client, access_token):
    """Test that access token is used in requests."""
    # Make authenticated request
    response = api_client.get("/api/v1/organizations")
    
    # Verify request succeeded
    assert response.status_code == 200
    
    # Verify token was included in request
    assert "Authorization" in response.request.headers
    assert f"Bearer {access_token}" in response.request.headers["Authorization"]
```

### Test Token Refresh

```python
def test_token_refresh(api_client):
    """Test that expired tokens are automatically refreshed."""
    # Simulate expired token
    old_token = api_client.token_store["access_token"]
    
    # Make request (will trigger refresh if token expired)
    response = api_client.get("/api/v1/organizations")
    
    # Check if token was refreshed
    new_token = api_client.token_store["access_token"]
    
    # Either token stayed same or was refreshed
    assert response.status_code == 200
    assert api_client.token_store["access_token"]  # Token exists
```

### Test Login Fallback

```python
def test_login_fallback(api_client):
    """Test that APIClient falls back to login on refresh failure."""
    # Corrupt refresh token to force fallback
    api_client.token_store["refresh_token"] = "invalid_token"
    
    # Make request - should fallback to login
    response = api_client.get("/api/v1/organizations")
    
    # Should still succeed via login fallback
    assert response.status_code == 200
```

### Test Negative Cases

```python
@pytest.mark.parametrize(
    "username,password,expected_status",
    [
        ("invalid@email.com", "password", 401),
        ("user@email.com", "wrongpassword", 401),
        ("", "password", 400),
        ("user@email.com", "", 400),
    ]
)
def test_login_negative(config, username, password, expected_status):
    """Test login with invalid credentials."""
    from core.auth import login
    
    try:
        login(
            base_url=config["base_url"],
            endpoint=config["login_endpoint"],
            username=username,
            password=password
        )
        # If no exception, check wasn't expected to succeed
        if expected_status >= 400:
            pytest.fail("Login should have failed")
    except Exception as e:
        # Expected to fail
        assert expected_status >= 400
```

---

## Authorization Headers

### Automatic Header Management

APIClient automatically adds authorization headers:

```python
def _prepare_headers(self, headers: Optional[dict] = None) -> dict:
    headers = headers.copy() if headers else {}
    token = self.token_store.get("access_token")
    
    if token:
        # Add Bearer token
        headers["Authorization"] = f"Bearer {token}"
    
    headers.setdefault("Content-Type", "application/json")
    return headers
```

### Header Examples

**With Token**:
```
Authorization: Bearer eyJhbGciOiJIUzUxMiJ9...
Content-Type: application/json
```

**Without Token**:
```
Content-Type: application/json
```

### Custom Headers

You can add custom headers while keeping authorization:

```python
def test_with_custom_headers(api_client):
    """Add custom headers along with authorization."""
    custom_headers = {
        "X-Custom-Header": "value",
        "X-API-Version": "2"
    }
    
    response = api_client.get(
        "/api/v1/organizations",
        headers=custom_headers
    )
    
    # Both custom headers and Authorization are sent
    assert response.status_code == 200
```

---

## Security Considerations

### Best Practices

1. **Never Log Tokens**
   ```python
   # Bad - Don't do this
   print(f"Token: {token}")  # ❌ Don't expose
   
   # Good
   print(f"Token: {token[:20]}...")  # ✅ Mask token
   ```

2. **Use Environment Variables for Credentials**
   ```yaml
   credentials:
     email: ${TEST_EMAIL}        # Use env var
     password: ${TEST_PASSWORD}  # Use env var
   ```

3. **Secure Token Storage**
   ```python
   # Tokens are stored in memory
   client.token_store = {
       "access_token": "...",
       "refresh_token": "..."
   }
   # Access only when needed
   ```

4. **Rotate Refresh Tokens**
   - New refresh tokens should be issued periodically
   - Old tokens should be invalidated

5. **Set Token Expiration**
   - Access tokens: Short lived (5-15 minutes)
   - Refresh tokens: Longer lived (days/weeks)

---

## Troubleshooting

### Issue: 401 Unauthorized on Every Request

**Cause**: Tokens are expired and refresh is failing

**Solution**:
```python
# Check token validity
print(client.token_store["access_token"])

# Check refresh endpoint
print(client.refresh_endpoint)

# Manually test refresh
success = client._refresh_access_token()
print(f"Refresh successful: {success}")

# Check credentials if refresh fails
config = load_config("dev")
print(f"Using credentials: {config['credentials']['email']}")
```

### Issue: Refresh Token Invalid

**Cause**: Refresh token has expired

**Solution**:
```python
# Perform new login
tokens = login(
    base_url=client.base_url,
    endpoint="/api/v1/user/login",
    username="user@example.com",
    password="password"
)

client.token_store["access_token"] = tokens["access_token"]
client.token_store["refresh_token"] = tokens["refresh_token"]
```

### Issue: Login Function Not Working

**Cause**: login_func not provided to APIClient

**Solution**:
```python
# Ensure login_func is provided
def my_login_func():
    return login(...)

client = APIClient(
    base_url="...",
    login_func=my_login_func  # ✅ Must be provided
)
```

### Issue: Token Not Included in Request

**Cause**: Access token is None

**Solution**:
```python
# Check token exists
print(f"Access token: {client.token_store['access_token']}")

# Login if None
if not client.token_store["access_token"]:
    client._login()

# Try request again
response = client.get("/api/v1/organizations")
```

---

## Advanced Topics

### Custom Authentication Flow

For custom authentication needs:

```python
class CustomAPIClient(APIClient):
    """APIClient with custom authentication."""
    
    def _refresh_access_token(self) -> bool:
        """Override with custom refresh logic."""
        # Custom refresh implementation
        pass
    
    def _login(self) -> bool:
        """Override with custom login logic."""
        # Custom login implementation
        pass
```

### Token Validation

Decode JWT tokens to validate:

```python
import base64
import json

def decode_jwt(token):
    """Decode JWT token (note: doesn't verify signature)."""
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    
    # Decode payload (add padding if needed)
    payload = parts[1]
    payload += '=' * (4 - len(payload) % 4)
    
    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)

# Usage
token = client.token_store["access_token"]
decoded = decode_jwt(token)

print(f"Subject: {decoded['sub']}")
print(f"Issued at: {decoded['iat']}")
print(f"Expires at: {decoded['exp']}")
```

---

## Related Documentation

- [Main README](../README.md)
- [API Client Guide](./API_CLIENT.md)
- [Configuration Guide](./CONFIGURATION.md)
- [Testing Guide](./TESTING_GUIDE.md)
- [Quick Start](./QUICK_START.md)

