import allure
from playwright.sync_api import Page, Response

STATIC_EXTENSIONS = (".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".woff", ".woff2", ".ttf", ".ico", ".map")
STATIC_CONTENT_TYPES = ("image/", "font/", "text/css", "application/javascript")


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.on("response", self._capture_network)
        self.page.on("requestfailed", self._capture_failed_request)

    def _capture_network(self, response: Response):
        url = response.url
        if any(url.endswith(ext) for ext in STATIC_EXTENSIONS):
            return
        content_type = response.headers.get("content-type", "")
        if any(content_type.startswith(ct) for ct in STATIC_CONTENT_TYPES):
            return
        try:
            body = response.text()
        except Exception:
            body = "<could not read body>"
        name = f"{response.request.method} {url} → {response.status}"
        allure.attach(body, name=name, attachment_type=allure.attachment_type.TEXT)

    def _capture_failed_request(self, request):
        allure.attach(
            f"FAILED: {request.method} {request.url}\nReason: {request.failure}",
            name=f"FAILED REQUEST: {request.url}",
            attachment_type=allure.attachment_type.TEXT,
        )

    def screenshot(self, name: str):
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
