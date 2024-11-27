import pytest
from playwright.sync_api import Page, Playwright

from element_getter import ElementGetter
from element_interactor import ElementInteractor


def element_tester(
    page: Page,
    element_interactor: ElementInteractor,
    element_getter: ElementGetter,
    url: str,
    interact_dict: dict,
    testing_element: tuple,
    testing_value,
    error: str,
) -> None:
    """
    interact_dict - dictionar ce trebuie sa aiba structura - "function_to_call" : {"locator": "locator_value", "argument_1": "value1"}
                  - va rezulta intr-un call de tipul element_interactor.function_to_call(locator_value, value1)
    testing_element - tuple ce contine (functiion_to_call, locator)
                  - va rezulta intr-un call de tipul element_getter.function_to_call(locator_value)
    """

    page.goto(url)

    if not check_interactor_dict_validity(interact_dict):
        print(
            "Your interactor_dict is not valid. Every key should be a function name from ElementInteractor Class"
        )
        return

    if not hasattr(element_getter, testing_element[0]):
        print(
            "Your testing_element is not valid. First arg should be a function name from ElementGetter Class"
        )
        return

    try:
        for action in interact_dict.keys():
            getattr(element_interactor, action)(**interact_dict[action])

        actual_value = getattr(element_getter, testing_element[0])(testing_element[1])
    except Exception as e:
        print(str(e))

    assert actual_value == testing_value, error


def check_interactor_dict_validity(interactor_dict: dict) -> bool:
    return True


def form_tester():
    pass
