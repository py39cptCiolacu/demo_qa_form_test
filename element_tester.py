import pytest
from playwright.sync_api import Page, Playwright

from element_getter import ElementGetter
from element_interactor import ElementInteractor


class ElementTester:

    def __init__(
        self,
        page: Page,
        url: str,
        interact_dict: dict,
        testing_element: tuple,
        testing_value,
    ):
        self.page = page
        self.url = url
        self.interact_dict = interact_dict
        self.testing_element = testing_element
        self.testing_value = testing_value
        self.element_interactor = ElementInteractor(self.page)
        self.element_getter = ElementGetter(self.page)

    def test(self) -> None:
        """
        interact_dict - dictionar ce trebuie sa aiba structura - "function_to_call" : {"locator": "locator_value", "argument_1": "value1"}
                    - va rezulta intr-un call de tipul element_interactor.function_to_call(locator_value, value1)
        testing_element - tuple ce contine (functiion_to_call, locator)
                    - va rezulta intr-un call de tipul element_getter.function_to_call(locator_value)
        """

        self.page.goto(self.url)

        if not self.check_interactor_dict_validity(self.interact_dict):
            print(
                "Your interactor_dict is not valid. Every key should be a function name from ElementInteractor Class"
            )
            return

        if not hasattr(self.element_getter, self.testing_element[0]):
            print(
                "Your testing_element is not valid. First arg should be a function name from ElementGetter Class"
            )
            return

        try:
            for action in self.interact_dict.keys():
                getattr(self.element_interactor, action)(**self.interact_dict[action])

            actual_value = getattr(self.element_getter, self.testing_element[0])(
                self.testing_element[1]
            )
        except Exception as e:
            print(str(e))

        assert actual_value == self.testing_value, f"Expected value was {self.testing_value} but we got {actual_value}"

    def check_interactor_dict_validity(self, interactor_dict: dict) -> bool:
        return True
