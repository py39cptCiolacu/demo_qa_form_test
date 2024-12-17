from playwright.sync_api import Page, ElementHandle, Locator
import time

IDENTIFIERS = ["input", "textarea"]

class CompleteForm:

    def __init__(self, form_dict: dict, page: Page, test_with_modal: bool = False) -> None:
        self.form_dict = form_dict
        self.page = page
        self.test_with_modal = test_with_modal

    def test(self) -> None:
        self.find_type_and_take_action()
        self.__check_by_type()
        time.sleep(3)

    def find_type_and_take_action(self):
    ####  Might not been always the case
        form_element = self.page.locator("#userForm")
        rows: list[ElementHandle] = form_element.locator(".mt-2.row").all()
    ####

        dict_row_label = self.__find_row_label_pairs(rows)

        labels_to_iterate = []
        for label in dict_row_label.keys():
            if label in self.form_dict.keys():
                labels_to_iterate.append(label)


        for label in labels_to_iterate:
            row = dict_row_label[label]
            print(row)
            for identifier in IDENTIFIERS:
                if row.locator(identifier).nth(0).is_visible():
                    identifier_element = row.locator(identifier).nth(0)
                    if identifier == "input":
                        typ = identifier_element.get_attribute("type")
                        identifier_type = "input-" + typ
                    else:
                        identifier_type = identifier
                    break

            assert identifier_type

            self.__match_actions(label, identifier_type, row)

    def __find_row_label_pairs(self, rows: list[Locator]) -> dict:
        change_key_dict = {"Male": "Gender", "Mobile(10 Digits)": "Mobile"}
        dict_row_label = {}
        for row in rows:
            if not row.locator("label").first.is_visible():
                continue
            label = row.locator("label").first
            label_text = label.inner_text()
            if label_text in change_key_dict:
                label_text = change_key_dict.get(label_text)
            dict_row_label[label_text] = row

        return dict_row_label

    def __match_actions(self, key: str, identifier_type: Locator, row: Locator) -> None:
        match identifier_type:
            case "input-text":
                self.__case_input_text(key, row)
            case "input-email":
                self.__case_input_text(key, row)
            case "input-radio":
                to_be_checked = self.form_dict.get(key)
                row.locator(f"label >> text='{to_be_checked}'").click()
            case "input-checkbox":
                to_be_checked_elements = self.form_dict.get(key)
                for to_be_checked_element in to_be_checked_elements:
                    row.locator(f"label:has-text('{to_be_checked_element}')").click()
            case "input-file":
                pass
            case "textarea":
                value = self.form_dict.get(key)
                row.locator("textarea").fill(value)
            case _:
                raise TypeError(f"This {identifier_type} is not supported")

    def __case_input_text(self, key: str, row: Locator) -> None:
        inputs = row.locator("input").all()
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
            results_sector = self.page.locator("#output")
            results = results_sector.locator("p").all()

            if len(results) > 0:
                self.__check_form_id_output(results)

    def __check_form_id_output(self, results: list[Locator]) -> None:
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
        modal = self.page.locator(".modal-body")
        assert modal

        results = {}

        trs = modal.locator("tr").all()

        for tr in trs:
            tds = tr.locator("td").all()
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
