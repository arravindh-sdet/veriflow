class BasePage:
    """Common helpers shared by Playwright page objects."""

    def __init__(self, page, base_url=""):
        self.page = page
        self.base_url = base_url.rstrip("/") if base_url else ""

    def open(self, path=""):
        if not self.base_url:
            raise ValueError("A base URL is required before calling open().")

        normalized_path = path if path.startswith("/") else f"/{path}" if path else ""
        self.page.goto(f"{self.base_url}{normalized_path}", wait_until="domcontentloaded")
