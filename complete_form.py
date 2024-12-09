from playwright.async_api import Page, ElementHandle
from navigator import navigate
import time

IDENTIFIERS = ["input", "textarea"]

class CompleteForm:

    def __init__(self, form_dict: dict, page: Page) -> None:
        self.destination = form_dict.get("destination")
        form_dict.pop("destination")

        self.form_dict = form_dict
        self.page = page

    def test(self) -> None:
        self.page = navigate(self.page, self.destination)
        self.__find_type()
        self.__match_checking()

    def __find_type(self):
    ####  Might not been always the case
        form_element = self.page.query_selector("#userForm")
        rows: list[ElementHandle] = form_element.query_selector_all(".mt-2.row")
    ####

        for row in rows[:-1]:
            label: ElementHandle = row.query_selector("label")

            if label:
                label_text = label.inner_text()
            else:
                raise ValueError("There is no label")

            for identifier in IDENTIFIERS:
                identifier_element = row.query_selector(identifier)
                if identifier_element:
                    break

            if not identifier_element:
                raise TypeError(f"{identifier} was not found")

            self.__match_actions(label_text, identifier_element)

    def __match_actions(self, key: str, identifier: ElementHandle):
        match identifier.evaluate("el => el.tagName").lower():
            case "input":
                identifier_id = identifier.get_attribute("id")
                self.page.locator(f"#{identifier_id}").fill(value = self.form_dict.get(key))
            case "textarea":
                identifier_id = identifier.get_attribute("id")
                self.page.locator(f"#{identifier_id}").fill(value=self.form_dict.get(key))
            case _:
                raise TypeError(f"{identifier} should be part of {IDENTIFIERS}")

    def __match_checking(self) -> None:
        self.page.click("#submit")

        results_sector: ElementHandle = self.page.query_selector("#output")
        results: list[ElementHandle] = results_sector.query_selector_all("p")

        if len(results) > 0:
            self.__check_form_id_output(results)


    def __check_form_id_output(self, results: list[ElementHandle]) -> None:
        for result in results:
            inner_text: str = result.inner_text()
            inner_text_as_list = inner_text.split(":")

            inner_text_as_list[0] = inner_text_as_list[0].strip()
            inner_text_as_list[1] = inner_text_as_list[1].strip()

            if inner_text_as_list[0] == "Name":
                inner_text_as_list[0] = "Full Name"

            if inner_text_as_list[0] == "Permananet Address":
                inner_text_as_list[0] = "Permanent Address"

            assert self.form_dict.get(inner_text_as_list[0]) == inner_text_as_list[1], f"Expected {self.form_dict.get(inner_text_as_list[0])} but got {inner_text_as_list[1]}"

