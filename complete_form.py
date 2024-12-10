from playwright.async_api import Page, ElementHandle
from navigator import navigate
import time

IDENTIFIERS = ["input", "textarea"]

class CompleteForm:

    def __init__(self, form_dict: dict, page: Page, test_with_modal: bool = False) -> None:

        if "destination" in form_dict.keys():
            self.destination = form_dict.get("destination")
            form_dict.pop("destination")

        self.form_dict = form_dict
        self.page = page
        self.test_with_modal = test_with_modal

    def test(self) -> None:
        self.page = navigate(self.page, self.destination)
        self.find_type_and_action()
        self.__check_by_type()
        time.sleep(3)

    def find_type_and_action(self):
    ####  Might not been always the case
        form_element = self.page.query_selector("#userForm")
        rows: list[ElementHandle] = form_element.query_selector_all(".mt-2.row")
    ####

        for row in rows:
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

    def __match_actions(self, key: str, identifier_type: ElementHandle, row: ElementHandle) -> None:
        change_key_dict = {"Male": "Gender", "Mobile(10 Digits)": "Mobile"}
        if key in change_key_dict:
            key = change_key_dict.get(key)

        match identifier_type:
            case "input-text":
                self.__case_input_text(key, row)
            case "input-radio":
                to_be_checked = self.form_dict.get(key)
                row.query_selector(f"label:has-text('{to_be_checked}')").click()
            case "input-checkbox":
                to_be_checked_elements = self.form_dict.get(key)
                for to_be_checked_element in to_be_checked_elements:
                    row.query_selector(f"label:has-text('{to_be_checked_element}')").click()
            case "input-file":
                pass
            case "textarea":
                value = self.form_dict.get(key)
                row.query_selector("textarea").fill(value)
            case _:
                raise TypeError(f"This {identifier_type} is not supported")

    def __case_input_text(self, key: str, row: ElementHandle) -> None:
        inputs = row.query_selector_all("input")
        if len(inputs) == 1:
            value = self.form_dict.get(key)
            inputs[0].fill(value)
            if inputs[0].get_attribute("aria-autocomplete") == "list":
                inputs[0].press("Tab")
        else:
            values = self.form_dict.get(key)
            i= 0
            for input in inputs:
                input.fill(values[i])
                if input.get_attribute("aria-autocomplete") == "list":
                    input.press("Tab")
                i += 1

    def __check_by_type(self) -> None:
        self.page.click("#submit")

        if self.test_with_modal:
            results = self.__get_modal_results()
            self.__check_modal_results(results)
        else:
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

    def __get_modal_results(self):
        modal = self.page.query_selector(".modal-body")
        assert modal

        results = {}

        trs = modal.query_selector_all("tr")

        for tr in trs:
            tds = tr.query_selector_all("td")
            if len(tds) >= 2:
                key = tds[0].inner_text().strip()
                value = tds[1].inner_text().strip()
                results[key] = value
        print(results)

        return results

    def __check_modal_results(self, results: dict):
        change_key_dict = {"Student Name": "Name", "Student Email": "Email", "Address": "Current Address"}

        for key in results.keys():

            form_key = key

            if key in change_key_dict.keys():
                form_key = change_key_dict.get(key)

            if form_key not in self.form_dict.keys():
                print(f"{key} is missing")
                continue

            if type(self.form_dict.get(form_key)) == list:
                temp_results_as_list = results.get(key).replace(',', '').split()

                print(f"Now testing {key} with {results.get(key)} AND {self.form_dict.get(form_key)}")
                for temp_result_as_list in temp_results_as_list:
                    assert temp_result_as_list in self.form_dict.get(form_key), f"{temp_results_as_list} is not in {self.form_dict.get(key)}"

                continue

            print(f"Now testing {key} with {results.get(key)} AND {self.form_dict.get(form_key)}")
            assert results.get(key) ==  self.form_dict.get(form_key)
