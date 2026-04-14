import re

import allure
import pytest

playwright_sync_api = pytest.importorskip("playwright.sync_api")
expect = playwright_sync_api.expect

from ui.pages.base_page import BasePage


@pytest.mark.ui
@allure.feature("UI")
@allure.story("Smoke")
def test_live_ui_homepage_loads(ui_page, ui_base_url):
    if not ui_base_url:
        pytest.skip(
            "Set ui_base_url in config/dev.local.yaml or pass --ui-base-url to run live UI smoke tests."
        )

    base_page = BasePage(ui_page, ui_base_url)
    base_page.open()

    expect(ui_page.locator("body")).to_be_visible()
    expect(ui_page).to_have_title(re.compile(r".+"))
