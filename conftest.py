import pytest
from playwright.sync_api import Page, Playwright

from element_interactor import ElementInteractor
from element_getter import ElementGetter


@pytest.fixture
def page(playwright: Playwright, request) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    browser.close()


@pytest.fixture
def element_interactor(page: Page) -> ElementInteractor:
    return ElementInteractor(page=page)


@pytest.fixture
def element_getter(page: Page) -> ElementGetter:
    return ElementGetter(page)