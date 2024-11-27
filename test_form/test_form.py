import pytest
from playwright.sync_api import Page, Playwright

from element_tester import ElementTester

URL = "https://demoqa.com/automation-practice-form"


def test_first_name(page: Page) -> None:

    interact_dict = {"fill_textbox": {"locator": "#firstName", "value": "Test Test"}}
    testing_element = ("get_input_text", "#firstName")
    testing_value = "Test Test"

    element_tester = ElementTester(
        page=page,
        url=URL,
        interact_dict=interact_dict,
        testing_element=testing_element,
        testing_value=testing_value,
    )

    element_tester.test()


def test_last_name(page: Page) -> None:

    interact_dict = {"fill_textbox": {"locator": "#lastName", "value": "Test"}}
    testing_element = ("get_input_text", "#lastName")
    testing_value = "Test"

    element_tester = ElementTester(
        page=page,
        url=URL,
        interact_dict=interact_dict,
        testing_element=testing_element,
        testing_value=testing_value,
    )

    element_tester.test()
