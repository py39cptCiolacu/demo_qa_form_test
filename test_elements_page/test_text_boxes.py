
from playwright.async_api import Page
from element_interactor import ElementInteractor
from element_getter import ElementGetter

URL = "https://demoqa.com/radio-button"

def test_full_name(page: Page, element_interactor: ElementInteractor, element_getter: ElementGetter):
    page.goto(URL)
    element_interactor.fill_textbox("#userName", "Test Test")
    assert element_getter.get_input_text("#userName") == "Test Test"
