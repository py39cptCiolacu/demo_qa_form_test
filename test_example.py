import pytest
from playwright.sync_api import Page

from element_checker import ElementInteractor

URL = "https://demoqa.com/"

@pytest.fixture
def element_interactor(page: Page) -> ElementInteractor:
    return ElementInteractor(base_url=URL, page=page)

def test_full_name(element_interactor: ElementInteractor) -> None:
    name = "Test Test"
    filled_value = element_interactor.fill_textbox("text-box", locator="#userName", value=name)
    assert filled_value == name, f"Expected {name} but got {filled_value}"

def test_email(element_interactor: ElementInteractor) -> None:
    email = "test@test.com"
    filled_value = element_interactor.fill_textbox("text-box", locator="#userEmail", value=email)
    assert filled_value == email, f"Expected {email} but got {filled_value}"