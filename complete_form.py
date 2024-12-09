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
        # self.__match_checking()

    def __find_type(self):
    ####  Might not been always the case
        form_element = self.page.query_selector("#userForm")
        rows: list[ElementHandle] = form_element.query_selector_all(".mt-2.row")
    ####

        for row in rows[:-1]:
            label: ElementHandle = row.query_selector("label")
            assert label

            for identifier in IDENTIFIERS:
                identifier_element = row.query_selector(identifier)
                if identifier_element:
                    if identifier == "input":
                        type = identifier_element.get_attribute("type")
                        identifier_type = "input-" + type
                    else:
                        identifier_type = identifier
                    break

            assert identifier_type

            self.__match_actions(label.inner_text(), identifier_type, row)

    def __match_actions(self, key: str, identifier_type: ElementHandle, row: ElementHandle):
        match identifier_type:
            case "input-text":
                inputs = row.query_selector_all("input")
                if len(inputs) == 1:
                    value = str(self.form_dict.get(key))
                    print(value)
                    inputs[0].fill(value)
                else:
                    values = self.form_dict.get(key)
                    i= 0
                    for input in inputs:
                        input.fill(values[i])
                        i += 1
            case "input-radio":
                if key == "Male":
                    key = "Gender"
                to_be_checked = self.form_dict.get(key)
                row.query_selector(f"label:has-text('{to_be_checked}')").click()
            case "input-checkbox":
                to_be_checked_elements = self.form_dict.get(key)
                for to_be_checked_element in to_be_checked_elements:
                    print(type(to_be_checked_element))
                    row.query_selector(f"label:has-text('{to_be_checked_element}')")
            case "textarea":
                value = self.form_dict.get(key)
                row.query_selector("textarea").fill(value)
                time.sleep(7)
            case "input-file":
                pass
            case _:
                raise TypeError(f"This {identifier_type} is not supported")

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

