# Documentation Index

Welcome to the COMS Pytest Documentation! This index helps you find the right documentation for your needs.

---

## 📚 Documentation Files

### Getting Started

- **[Quick Start Guide](QUICK_START.md)** ⚡
  - 5-minute setup and first test
  - Basic commands and common patterns
  - Troubleshooting quick reference
  - **Start here if you're new!**

- **[Main README](../README.md)** 📖
  - Complete project overview
  - Feature list and project structure
  - Installation and configuration
  - All documentation links

---

### Core Documentation

- **[API Client Guide](API_CLIENT.md)** 🔌
  - Complete APIClient reference
  - All methods and parameters
  - Token management details
  - Error handling and debugging
  - **Read this to understand how to make API calls**

- **[Testing Guide](TESTING_GUIDE.md)** ✅
  - How to write tests
  - Test structure and patterns
  - Parametrization and fixtures
  - Allure integration
  - Best practices
  - **Read this to learn how to write effective tests**

- **[Authentication & Token Management](AUTHENTICATION.md)** 🔐
  - Complete authentication flow
  - Login process details
  - Token refresh mechanism
  - Security best practices
  - **Read this to understand authentication**

---

### Configuration & Setup

- **[Configuration Guide](CONFIGURATION.md)** ⚙️
  - YAML configuration files
  - Environment setup (dev, qa, prod)
  - Configuration loading and usage
  - Best practices for managing configs
  - **Read this to set up environments**

- **[Fixtures Reference](FIXTURES.md)** 🎯
  - All available fixtures
  - Creating custom fixtures
  - Fixture scopes and parameters
  - Common fixture patterns
  - **Read this to learn about fixtures**

---

## 🎯 Quick Navigation by Task

### I want to...

#### **Run tests quickly**
→ Start with [Quick Start Guide](QUICK_START.md)
```bash
pytest
pytest --env dev
pytest --html=reports/report.html
```

#### **Write a new test**
→ Read [Testing Guide](TESTING_GUIDE.md)
→ Check examples in `tests/` directory
```python
def test_example(api_client):
    response = api_client.get("/api/v1/resource")
    assert response.status_code == 200
```

#### **Make API requests**
→ Read [API Client Guide](API_CLIENT.md)
→ Use the `api_client` fixture
```python
def test_with_api(api_client):
    response = api_client.post("/api/v1/endpoint", json=payload)
    assert response.status_code == 200
```

#### **Understand authentication**
→ Read [Authentication Guide](AUTHENTICATION.md)
→ Check `core/auth.py` and `core/api_client.py`
```python
# Token refresh happens automatically
response = api_client.get("/api/v1/resource")  # Retries on 401
```

#### **Set up a new environment**
→ Read [Configuration Guide](CONFIGURATION.md)
1. Create `config/new_env.yaml`
2. Run tests with `pytest --env new_env`

#### **Use fixtures**
→ Read [Fixtures Reference](FIXTURES.md)
→ Check existing fixtures in `conftest.py`
```python
def test_with_fixtures(api_client, config, auth_tokens):
    pass
```

#### **Generate reports**
→ See Quick Start Guide
```bash
pytest --html=reports/report.html
pytest --alluredir=allure-results
allure serve allure-results
```

#### **Debug a failing test**
→ Read [API Client Guide](API_CLIENT.md) troubleshooting
→ Use `pytest -v -s` for verbose output
```bash
pytest tests/file.py::test_name -v -s --log-cli-level=DEBUG
```

---

## 📋 Documentation by Topic

### Authentication & Tokens
- [Authentication Guide](AUTHENTICATION.md) - Complete auth flow
- [API Client Guide](API_CLIENT.md) - Token management section
- [Quick Start](QUICK_START.md) - Token basics

### Making API Requests
- [API Client Guide](API_CLIENT.md) - All methods
- [Testing Guide](TESTING_GUIDE.md) - Response assertions
- [Quick Start](QUICK_START.md) - Basic examples

### Writing Tests
- [Testing Guide](TESTING_GUIDE.md) - Complete guide
- [Quick Start](QUICK_START.md) - Simple examples
- [Fixtures Reference](FIXTURES.md) - Using fixtures

### Configuration
- [Configuration Guide](CONFIGURATION.md) - YAML files
- [Quick Start](QUICK_START.md) - Setup steps
- [Main README](../README.md) - Overview

### Fixtures
- [Fixtures Reference](FIXTURES.md) - Complete guide
- [Testing Guide](TESTING_GUIDE.md) - Using fixtures in tests
- [Main README](../README.md) - Available fixtures

### Reports & Logging
- [Quick Start](QUICK_START.md) - Report generation
- [Testing Guide](TESTING_GUIDE.md) - Allure integration
- [Main README](../README.md) - Reporting section

### Troubleshooting
- [Quick Start](QUICK_START.md) - Common issues
- [API Client Guide](API_CLIENT.md) - Debug guide
- [Authentication Guide](AUTHENTICATION.md) - Auth issues
- [Configuration Guide](CONFIGURATION.md) - Config issues

---

## 🚀 Common Tasks

### Task 1: Run Your First Test (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run tests
pytest

# 3. View results
# Tests output shown in terminal
```

**Docs**: [Quick Start](QUICK_START.md)

---

### Task 2: Write a New Test (5 minutes)

```python
# tests/my_test.py
import pytest

def test_create_resource(api_client):
    """Create a resource."""
    payload = {"name": "Test"}
    response = api_client.post("/api/v1/resource", json=payload)
    assert response.status_code == 200
```

```bash
pytest tests/my_test.py -v
```

**Docs**: [Testing Guide](TESTING_GUIDE.md), [API Client Guide](API_CLIENT.md)

---

### Task 3: Set Up New Environment (3 minutes)

```yaml
# config/staging.yaml
base_url: "https://staging.example.com"
login_endpoint: "/api/v1/user/login"
refresh_endpoint: "/api/v1/user/refreshToken"
credentials:
  email: "staging@example.com"
  password: "password"
```

```bash
pytest --env staging
```

**Docs**: [Configuration Guide](CONFIGURATION.md)

---

### Task 4: Generate Reports (2 minutes)

```bash
# HTML Report
pytest --html=reports/report.html --self-contained-html

# Allure Report
pytest --alluredir=allure-results
allure serve allure-results
```

**Docs**: [Quick Start](QUICK_START.md), [Main README](../README.md)

---

### Task 5: Debug Failing Test (5 minutes)

```bash
# Verbose output with logs
pytest tests/file.py::test_name -v -s

# Debug with breakpoint
pytest tests/file.py::test_name -v -s --pdb

# Detailed logging
pytest tests/file.py::test_name --log-cli-level=DEBUG
```

**Docs**: [API Client Guide](API_CLIENT.md), [Quick Start](QUICK_START.md)

---

## 📖 Documentation Overview

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [Quick Start](QUICK_START.md) | Get started quickly | 5 min |
| [Main README](../README.md) | Project overview | 15 min |
| [Testing Guide](TESTING_GUIDE.md) | Write tests | 20 min |
| [API Client Guide](API_CLIENT.md) | Make requests | 25 min |
| [Authentication](AUTHENTICATION.md) | Auth & tokens | 20 min |
| [Configuration](CONFIGURATION.md) | Setup environments | 15 min |
| [Fixtures](FIXTURES.md) | Use fixtures | 20 min |

---

## 🎓 Learning Paths

### Path 1: Complete Beginner
1. [Quick Start](QUICK_START.md) - Get it running
2. [Testing Guide](TESTING_GUIDE.md) - Learn to test
3. [API Client Guide](API_CLIENT.md) - Make requests
4. [Main README](../README.md) - Full overview

### Path 2: I Know pytest
1. [API Client Guide](API_CLIENT.md) - API specifics
2. [Configuration Guide](CONFIGURATION.md) - Setup
3. [Authentication Guide](AUTHENTICATION.md) - Auth details
4. [Fixtures Reference](FIXTURES.md) - Advanced fixtures

### Path 3: I Know API Testing
1. [Quick Start](QUICK_START.md) - Setup
2. [Main README](../README.md) - Overview
3. [Configuration Guide](CONFIGURATION.md) - Env config
4. [Testing Guide](TESTING_GUIDE.md) - Best practices

---

## 💡 Key Concepts

### Fixtures
Reusable test setup functions. Use `api_client`, `config`, `auth_tokens`, etc.

**Learn more**: [Fixtures Reference](FIXTURES.md)

### API Client
Main class for making HTTP requests with automatic token refresh.

**Learn more**: [API Client Guide](API_CLIENT.md)

### Token Refresh
Automatic retry logic on 401 errors with token refresh.

**Learn more**: [Authentication Guide](AUTHENTICATION.md)

### Configuration
YAML-based environment config for dev, qa, prod environments.

**Learn more**: [Configuration Guide](CONFIGURATION.md)

### Allure Reports
Beautiful interactive test reports with trends and analytics.

**Learn more**: [Testing Guide](TESTING_GUIDE.md), [Main README](../README.md)

---

## 🔗 External Resources

- **[Pytest Documentation](https://docs.pytest.org/)** - pytest reference
- **[Requests Library](https://docs.python-requests.org/)** - HTTP client
- **[Allure Documentation](https://docs.qameta.io/allure/)** - Test reporting
- **[JSONSchema](https://json-schema.org/)** - Data validation
- **[PyYAML](https://pyyaml.org/)** - YAML parsing

---

## ❓ FAQ

### Q: Where do I start?
**A**: Start with [Quick Start Guide](QUICK_START.md) if new, or [Main README](../README.md) for overview.

### Q: How do I write tests?
**A**: Read [Testing Guide](TESTING_GUIDE.md) and check examples in `tests/` directory.

### Q: How do I make API calls?
**A**: Read [API Client Guide](API_CLIENT.md) and use the `api_client` fixture.

### Q: How do I set up a new environment?
**A**: Read [Configuration Guide](CONFIGURATION.md) and create a new YAML config file.

### Q: How do I use fixtures?
**A**: Read [Fixtures Reference](FIXTURES.md) and check `conftest.py` examples.

### Q: How do I generate reports?
**A**: See [Quick Start](QUICK_START.md) or [Main README](../README.md) reporting section.

### Q: How does token refresh work?
**A**: Read [Authentication Guide](AUTHENTICATION.md) complete auth flow section.

### Q: What if a test fails?
**A**: Check [API Client Guide](API_CLIENT.md) troubleshooting section.

---

## 📝 Document Structure

Each documentation file includes:

- **Overview** - What the document covers
- **Table of Contents** - Easy navigation
- **Detailed Sections** - Complete information
- **Examples** - Real code samples
- **Troubleshooting** - Common issues and solutions
- **Related Documentation** - Links to other docs

---

## 🔄 Feedback & Updates

Documentation is maintained alongside code. If you find:
- Missing information
- Unclear explanations
- Outdated examples

Please report so it can be improved!

---

## 📞 Support

### Getting Help

1. **Check relevant documentation** - Use this index to find the right guide
2. **Search for keywords** - Each doc has a table of contents
3. **Look at code examples** - Examples are included in each guide
4. **Check test files** - `tests/` directory has real test examples

### Still Stuck?

- Check [Quick Start](QUICK_START.md) troubleshooting
- Review relevant guide's troubleshooting section
- Check test examples in `tests/` directory

---

## 📚 Complete File List

### Documentation Files (in `docs/` directory)
- `QUICK_START.md` - Quick start guide
- `TESTING_GUIDE.md` - How to write tests
- `API_CLIENT.md` - API client reference
- `AUTHENTICATION.md` - Auth & tokens
- `CONFIGURATION.md` - Configuration guide
- `FIXTURES.md` - Fixtures reference
- `INDEX.md` - This file

### Project Files
- `README.md` - Main project README
- `conftest.py` - Pytest fixtures
- `pytest.ini` - Pytest configuration
- `requirements.txt` - Dependencies

### Source Code
- `core/` - Framework core
- `tests/` - Test suites
- `config/` - Configuration files
- `helpers/` - Helper utilities
- `utilities/` - Test utilities

---

**Last Updated**: March 17, 2026  
**Version**: 1.0.0

Happy testing! 🚀

