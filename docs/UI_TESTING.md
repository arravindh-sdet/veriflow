# UI Testing with Playwright

## Overview

This project includes a Playwright-based UI automation layer alongside the existing API framework.

The UI setup includes:

- Shared pytest fixtures for browser, context, and page management
- Reusable Playwright page objects
- A self-contained local demo test for quick validation
- A live UI smoke-test pattern that runs against a configured `ui_base_url`

---

## Installation

Install project dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright browser binaries:

```bash
python -m playwright install chromium
```

You can install all supported browsers if needed:

```bash
python -m playwright install
```

---

## Configuration

Add the UI URL to your private local config:

```yaml
# config/dev.local.yaml
base_url: "https://your-private-api-url.com"
ui_base_url: "https://your-private-ui-url.com"
login_endpoint: "/api/v1/auth/login"
refresh_endpoint: "/api/v1/auth/refresh"
credentials:
  email: "your-email@example.com"
  password: "your-password"
```

You can also override the UI URL from the command line:

```bash
pytest tests/ui/test_live_ui_smoke.py --ui-base-url https://your-ui-app.com
```

---

## Available Fixtures

### `ui_base_url`

Returns the UI base URL from `--ui-base-url` or `config/<env>.yaml`.

### `ui_browser`

Launches a shared Playwright browser for the test session.

### `ui_context`

Creates an isolated browser context for each UI test.

### `ui_page`

Creates a new Playwright page for each UI test.

### `demo_ui_url`

Provides the file URL for the bundled demo page at `tests/ui/fixtures/demo_app.html`.

---

## Running UI Tests

Run the self-contained demo tests:

```bash
pytest tests/ui/test_demo_page.py -m ui
```

Run the live smoke test against a real application:

```bash
pytest tests/ui/test_live_ui_smoke.py -m ui --ui-base-url https://your-ui-app.com
```

Run UI tests in headed mode:

```bash
pytest tests/ui -m ui --headed
```

Choose a different browser:

```bash
pytest tests/ui -m ui --browser firefox
```

---

## Page Object Structure

Reusable Playwright page objects live under `ui/pages/`.

- `base_page.py` contains shared navigation helpers
- `demo_page.py` contains the sample demo page object

This structure is a good place to add real application pages such as login, dashboard, or organization management flows.
