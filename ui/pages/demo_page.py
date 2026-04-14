from ui.pages.base_page import BasePage


class DemoPage(BasePage):
    """Page object for the self-contained Playwright demo page."""

    def open_demo(self, demo_url):
        self.page.goto(demo_url, wait_until="domcontentloaded")

    @property
    def hero_title(self):
        return self.page.locator("[data-testid='hero-title']")

    @property
    def email_input(self):
        return self.page.locator("[data-testid='email']")

    @property
    def password_input(self):
        return self.page.locator("[data-testid='password']")

    @property
    def sign_in_button(self):
        return self.page.locator("[data-testid='sign-in']")

    @property
    def status_message(self):
        return self.page.locator("[data-testid='status']")

    def sign_in(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()
