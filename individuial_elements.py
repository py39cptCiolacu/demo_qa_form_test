import time

from playwright.sync_api import Page, ElementHandle

from navigator import navigate

from complete_form import CompleteForm

class IndividualElements:

    def __init__(self, type: str, form_dict: dict, page: Page) -> None:
        self.type = type
        self.form_dict = form_dict
        self.page = page
        self.checked = []

    def test(self):
        match self.type:
            case "Check Box":
                self.__press_checkboxes()
                self.__test_checkboxes()
            case "Radio Button":
                self.__press_radio_button()
                self.__test_radio_button()

    def __press_checkboxes(self):
        self.page.locator(".rct-option.rct-option-expand-all").click()

        for key in self.form_dict.get("Home").keys():
            directory_span = self.page.locator(f"span:text('{key}')")
            if not directory_span:
                raise ValueError(f"Directory Span with text {key} not found")

            directory_li = directory_span
            while directory_li and directory_li.evaluate('node => node.tagName.toLowerCase()') != "li":
                directory_li = directory_li.locator("xpath=..")
            assert directory_li.evaluate('node => node.tagName.toLowerCase()') == "li"

            self.__iterate_checkboxes(key, directory_li)


    def __iterate_checkboxes(self, key: str, directory_li, elements: list| dict = None):
        if not elements:
            elements = self.form_dict.get("Home").get(key)
        if type(elements) == list:
            if "*" in elements:
                directory_to_click = directory_li.locator(f"span.rct-title:has-text('{key}')")
                if not directory_to_click:
                    raise ValueError(f"Directory {key} not found")

                directory_to_click.click()

                checked_files = directory_li.locator(f"span.rct-title").all()
                for checked_file in checked_files:
                    if '.' in checked_file.inner_text():
                        base_name_file = checked_file.inner_text().rsplit('.', 1)[0]
                    else:
                        base_name_file = checked_file.inner_text()

                    base_name_file = base_name_file.replace(" ", "").lower()
                    self.checked.append(base_name_file)

                return

            for file in elements:
                file = directory_li.locator(f"span.rct-title:has-text('{file}')")
                assert file
                file.click()

                if '.' in file.inner_text():
                    base_name_file = file.inner_text().rsplit('.', 1)[0]
                else:
                    base_name_file = file.inner_text()

                base_name_file = base_name_file.replace(" ", "").lower()
                self.checked.append(base_name_file)

        elif type(elements) == dict:

            for sub_key in elements.keys():
                sub_directory_li = self.page.locator(f"span.rct-title:has-text('{key}')")
                # print(key, type(sub_directory_li))
                while sub_directory_li and sub_directory_li.evaluate("node => node.tagName.toLowerCase()") != "li":
                    sub_directory_li = sub_directory_li.locator("xpath=..")
                assert directory_li.evaluate('node => node.tagName.toLowerCase()') == "li"

                sub_elements = elements.get(sub_key)
                self.__iterate_checkboxes(sub_key, sub_directory_li, sub_elements)

    def __test_checkboxes(self):

        elements = self.page.locator("span.text-success").all()
        for element in elements:
            assert element.inner_text() in self.checked

    def __press_radio_button(self):
        key = list(self.form_dict.keys())[0]
        value = self.form_dict.get(key)
        interest_area = self.page.locator(f"div:has-text('{key}')")
        interest_area.locator("xpath=..")
        interest_area.locator(f"label:has-text('{value}')").click()

    def __test_radio_button(self):
        key = list(self.form_dict.keys())[0]
        result = self.page.locator(".text-success").inner_text()
        assert result == self.form_dict.get(key)