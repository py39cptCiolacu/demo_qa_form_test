from playwright.async_api import Page

from element_interactor import ElementInteractor
from element_getter import ElementGetter

URL = "https://demoqa.com/radio-button"


def test_yes(
    page: Page, element_interactor: ElementInteractor, element_getter: ElementGetter
):
    page.goto(URL)
    element_interactor.press_on_box("label[for='yesRadio']")
    assert element_getter.get_content_text(".text-success") == "Yes"
