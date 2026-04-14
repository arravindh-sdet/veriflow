# Configuration Guide

## Overview

The COMS Pytest framework uses YAML-based configuration files for managing environment-specific settings including API URLs, UI URLs, credentials, and endpoints.

---

## Table of Contents

1. [Configuration Structure](#configuration-structure)
2. [Environments](#environments)
3. [Configuration Files](#configuration-files)
4. [Loading Configuration](#loading-configuration)
5. [Using Configuration](#using-configuration)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Configuration Structure

### YAML Configuration Format

```yaml
# Base API URL
base_url: "https://api.example.com"
ui_base_url: "https://app.example.com"

# Endpoints
login_endpoint: "/api/v1/user/create/login"
refresh_endpoint: "/api/v1/user/create/refreshToken"

# Credentials
credentials:
  email: "user@example.com"
  password: "password123"

# Optional: Additional settings
timeout: 30
verify_ssl: true
```

### Configuration Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `base_url` | string | Yes | API base URL | `https://api.example.com` |
| `ui_base_url` | string | No | UI base URL for Playwright tests | `https://app.example.com` |
| `login_endpoint` | string | Yes | Login endpoint path | `/api/v1/user/login` |
| `refresh_endpoint` | string | Yes | Token refresh endpoint path | `/api/v1/user/refreshToken` |
| `credentials.email` | string | Yes | User email for authentication | `user@example.com` |
| `credentials.password` | string | Yes | User password | `SecurePass123!` |
| `timeout` | integer | No | Request timeout in seconds | `30` |
| `verify_ssl` | boolean | No | Verify SSL certificates | `true` |

---

## Environments

### Development (dev)

**File**: `config/dev.yaml`

Used for local development and testing.

```yaml
base_url: "https://api.example.com"
ui_base_url: ""
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  email: "your-email@example.com"
  password: "your-password"
```

For public repositories, store real credentials and any private UI URL in `config/dev.local.yaml`. The loader automatically prefers that private file over `config/dev.yaml`.

### Quality Assurance (qa)

**File**: `config/qa.yaml`

Used for QA testing on staging environment.

```yaml
base_url: "https://qa-api.example.com"
login_endpoint: "/api/v1/user/create/login"
refresh_endpoint: "/api/v1/user/create/refreshToken"
credentials:
  email: "qa-user@example.com"
  password: "QAPassword123!"
verify_ssl: true
timeout: 30
```

### Production (prod)

**File**: `config/prod.yaml`

Used for production testing.

```yaml
base_url: "https://api.example.com"
login_endpoint: "/api/v1/user/create/login"
refresh_endpoint: "/api/v1/user/create/refreshToken"
credentials:
  email: "prod-user@example.com"
  password: "ProdPassword123!"
verify_ssl: true
timeout: 60
```

---

## Configuration Files

### File Location

All configuration files are located in the `config/` directory:

```
config/
├── __init__.py
├── dev.yaml
├── qa.yaml
└── prod.yaml
```

### Creating New Environment

1. **Create new YAML file** in `config/` directory:
   ```bash
   touch config/staging.yaml
   ```

2. **Add configuration**:
   ```yaml
   base_url: "https://staging-api.example.com"
   login_endpoint: "/api/v1/user/create/login"
   refresh_endpoint: "/api/v1/user/create/refreshToken"
   credentials:
     email: "staging-user@example.com"
     password: "StagingPassword123!"
   ```

3. **Use in tests**:
   ```bash
   pytest --env staging
   ```

---

## Loading Configuration

### Configuration Loader

The `ConfigLoader` class loads YAML configuration files:

```python
# core/config_loader.py
import yaml
import os

def load_config(env):
    """Load configuration for specified environment."""
    path = os.path.join("config", f"{env}.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)
```

### Usage

```python
from core.config_loader import load_config

# Load development config
config = load_config("dev")

# Load QA config
config = load_config("qa")

# Load production config
config = load_config("prod")
```

### Programmatic Access

```python
config = load_config("dev")

# Access top-level fields
base_url = config["base_url"]
login_endpoint = config["login_endpoint"]

# Access nested fields
email = config["credentials"]["email"]
password = config["credentials"]["password"]

# Access optional fields with defaults
timeout = config.get("timeout", 30)
verify_ssl = config.get("verify_ssl", True)
```

---

## Using Configuration

### In Fixtures

```python
# conftest.py

@pytest.fixture(scope="session")
def config(request):
    """Load environment config once."""
    env = request.config.getoption("--env")
    return load_config(env)

@pytest.fixture(scope="session")
def api_client(config, auth_tokens):
    """Create API client with config."""
    client = APIClient(
        base_url=config["base_url"],
        access_token=auth_tokens["access_token"],
        refresh_token=auth_tokens["refresh_token"],
        refresh_endpoint=config.get("refresh_endpoint")
    )
    return client
```

### In Tests

```python
def test_with_config(config):
    """Use config in test."""
    assert config["base_url"]
    assert config["credentials"]["email"]

def test_with_multiple_configs(config):
    """Access multiple config values."""
    base_url = config["base_url"]
    email = config["credentials"]["email"]
    password = config["credentials"]["password"]
    
    # Use in test logic
    assert base_url.startswith("https://")
    assert "@" in email
```

### Environment-Specific Testing

```python
import pytest

def test_dev_only(config):
    """Test specific to dev environment."""
    if config["base_url"] == "https://api.example.com":
        # Dev-specific testing
        pass
    else:
        pytest.skip("Dev-only test")

def test_prod_only(config):
    """Test specific to production."""
    if "prod" in config["base_url"]:
        # Production-specific testing
        pass
    else:
        pytest.skip("Production-only test")
```

---

## Command Line Usage

### Specifying Environment

```bash
# Use development environment (default)
pytest --env dev

# Use QA environment
pytest --env qa

# Use production environment
pytest --env prod

# Use staging environment
pytest --env staging
```

### Command Examples

```bash
# Run tests on QA with verbose output
pytest --env qa -v -s

# Run specific test on production
pytest --env prod tests/auth/test_login.py::test_login

# Generate report for staging
pytest --env staging --html=reports/report.html --alluredir=allure-results

# Run with timeout for slow environments
pytest --env prod --timeout=60
```

---

## Best Practices

### 1. Never Commit Secrets

Use environment variables for sensitive data:

```yaml
# config/dev.yaml
base_url: "https://api.example.com"
login_endpoint: "/api/v1/user/login"
credentials:
  email: ${DEV_EMAIL}          # Use environment variable
  password: ${DEV_PASSWORD}    # Use environment variable
```

**Note**: If using Python to load with env vars, create a wrapper:

```python
import os
import yaml

def load_config(env):
    path = os.path.join("config", f"{env}.yaml")
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    
    # Replace environment variables
    config["credentials"]["email"] = os.getenv(
        "DEV_EMAIL",
        config["credentials"]["email"]
    )
    config["credentials"]["password"] = os.getenv(
        "DEV_PASSWORD",
        config["credentials"]["password"]
    )
    
    return config
```

### 2. Consistent Structure

Keep all environment config files with the same structure:

```yaml
# All files should have this structure
base_url: "..."
login_endpoint: "..."
refresh_endpoint: "..."
credentials:
  email: "..."
  password: "..."
```

### 3. Environment-Specific Values

Use appropriate values for each environment:

```yaml
# dev.yaml - Permissive settings
base_url: "https://dev.example.com"
verify_ssl: false
timeout: 30

# prod.yaml - Strict settings
base_url: "https://api.example.com"
verify_ssl: true
timeout: 60
```

### 4. Documentation

Document all available environments:

```yaml
# config/dev.yaml
# Development Environment Configuration
# Used for: Local development and testing
# Refresh: Daily
# Credentials: Personal dev account

base_url: "https://dev.example.com"
# ... rest of config
```

### 5. Validation

Validate configuration on load:

```python
def load_config(env):
    """Load and validate configuration."""
    config = load_config_file(env)
    
    # Validate required fields
    required_fields = ["base_url", "login_endpoint", "credentials"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    return config
```

---

## Advanced Configuration

### Using Environment-Specific Endpoints

```yaml
# config/dev.yaml
base_url: "https://dev.example.com"
endpoints:
  auth:
    login: "/api/v1/user/create/login"
    refresh: "/api/v1/user/create/refreshToken"
  organizations:
    create: "/api/v1/organizations/create"
    list: "/api/v1/organizations"
    update: "/api/v1/organizations/{id}"
```

### Access Endpoints

```python
def test_with_endpoints(config):
    """Use endpoints from config."""
    login_endpoint = config["endpoints"]["auth"]["login"]
    org_create = config["endpoints"]["organizations"]["create"]
    
    # Use in tests
    response = api_client.post(org_create, json=payload)
```

### Configuration Profiles

```yaml
# config/profiles.yaml
profiles:
  basic:
    timeout: 30
    verify_ssl: true
  advanced:
    timeout: 60
    verify_ssl: true
    retry_count: 3
```

---

## Troubleshooting

### Issue: Config File Not Found

**Error**: `FileNotFoundError: Config file not found: config/dev.yaml`

**Causes**:
- Config file doesn't exist
- Wrong environment name
- Wrong working directory

**Solution**:
```bash
# Check config files exist
ls config/

# Run from project root
cd /path/to/COMS_Pytest

# Check environment name
pytest --env dev  # Uses config/dev.yaml
```

### Issue: Invalid YAML Syntax

**Error**: `yaml.YAMLError: ...`

**Causes**:
- Invalid YAML syntax
- Incorrect indentation
- Missing quotes

**Solution**:
```yaml
# Good - Correct YAML
credentials:
  email: "user@example.com"
  password: "password123"

# Bad - Invalid YAML
credentials:
  email: user@example.com    # Missing quotes
  password: password123
```

### Issue: Missing Credentials

**Error**: `KeyError: 'credentials'`

**Causes**:
- Missing credentials section in config
- Typo in field name

**Solution**:
```yaml
# Ensure credentials section exists
credentials:
  email: "user@example.com"
  password: "password123"
```

### Issue: Cannot Load Module

**Error**: `ModuleNotFoundError: No module named 'yaml'`

**Solution**:
```bash
# Install PyYAML
pip install PyYAML
```

---

## Security Considerations

### 1. Never Commit Passwords

Add to `.gitignore`:
```
config/prod.yaml
config/local.yaml
*.key
*.secret
```

### 2. Use Environment Variables

```python
import os

email = os.getenv("TEST_EMAIL", "default@example.com")
password = os.getenv("TEST_PASSWORD", "")
```

### 3. File Permissions

```bash
# Restrict config file permissions
chmod 600 config/prod.yaml
```

### 4. Separate Credentials

```yaml
# config/dev.yaml - No actual credentials
base_url: "https://dev.example.com"
credentials:
  email: "${COMS_TEST_EMAIL}"
  password: "${COMS_TEST_PASSWORD}"
```

---

## Related Documentation

- [Main README](../README.md)
- [API Client Guide](./API_CLIENT.md)
- [Testing Guide](./TESTING_GUIDE.md)
- [Fixtures Reference](./FIXTURES.md)

---

## Quick Reference

### Load Configuration

```python
from core.config_loader import load_config
config = load_config("dev")
```

### Access Values

```python
base_url = config["base_url"]
email = config["credentials"]["email"]
timeout = config.get("timeout", 30)
```

### Run Tests

```bash
pytest --env dev
pytest --env qa
pytest --env prod
```

### Create New Environment

1. Create `config/new_env.yaml`
2. Add required fields
3. Run with `pytest --env new_env`
