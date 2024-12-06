import pytest
from playwright.sync_api import Page, Playwright

@pytest.fixture
def page(playwright: Playwright, request) -> Page:
    browser = playwright.chromium.launch(headless=False, channel="chrome")
    context = browser.new_context()
    page = context.new_page()
    yield page
    browser.close()
