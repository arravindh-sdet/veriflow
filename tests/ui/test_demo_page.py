import allure
import pytest

playwright_sync_api = pytest.importorskip("playwright.sync_api")
expect = playwright_sync_api.expect

from ui.pages.demo_page import DemoPage


@pytest.mark.ui
@allure.feature("UI")
@allure.story("Playwright Demo")
def test_demo_login_success(ui_page, demo_ui_url):
    demo_page = DemoPage(ui_page)

    demo_page.open_demo(demo_ui_url)
    expect(demo_page.hero_title).to_have_text("VeriFlow Demo Login")

    demo_page.sign_in("demo.user@example.com", "Playwright123")

    expect(demo_page.status_message).to_have_text("Welcome, demo.user@example.com")


@pytest.mark.ui
@allure.feature("UI")
@allure.story("Playwright Demo")
def test_demo_login_validation(ui_page, demo_ui_url):
    demo_page = DemoPage(ui_page)

    demo_page.open_demo(demo_ui_url)
    demo_page.sign_in("", "")

    expect(demo_page.status_message).to_have_text("Email and password are required.")
