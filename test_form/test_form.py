import pytest
from playwright.sync_api import Page, Playwright
from form_teste_utils import form_tester, element_tester

from element_getter import ElementGetter
from element_interactor import ElementInteractor

URL = "https://demoqa.com/automation-practice-form"


def test_form_element(
    page: Page, element_interactor: ElementInteractor, element_getter: ElementGetter
) -> None:

    interact_dict = {"fill_textbox": {"locator": "#firstName", "value": "Test Test"}}
    testing_element = ("get_input_text", "#firstName")
    testing_value = "Test Test"
    error = "Some Error"

    element_tester(
        page=page,
        element_interactor=element_interactor,
        element_getter=element_getter,
        url=URL,
        interact_dict=interact_dict,
        testing_element=testing_element,
        testing_value=testing_value,
        error=error,
    )
