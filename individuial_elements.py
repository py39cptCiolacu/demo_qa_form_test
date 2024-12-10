import time

from playwright.async_api import Page
from navigator import navigate

from complete_form import CompleteForm

class IndividualElements:

    def __init__(self, form_dict: dict, page: Page) -> None:
        self.destination = form_dict.get("destination")
        form_dict.pop("destination")

        self.form_dict = form_dict
        self.page = page
        self.checked = []

    def test(self):
        navigate(self.page, self.destination)
        match self.destination:
            case "Elements>Check Box":
                self.__press_checkboxes()
                self.__test_checkboxes()
            case "Elements>Radio Button":
                self.__press_radio_button()
                self.__test_radio_button()
            case "Elements>Web Tables":
                self.__clear_table()

                if "Add" in self.form_dict.keys():
                    self.__add_elements(self.form_dict.get("Add"))

                if "Delete" in self.form_dict.keys():
                    self.__delete_elements(self.form_dict.get("Delete"))

                time.sleep(10)

    def __press_checkboxes(self):
        self.page.locator(".rct-option.rct-option-expand-all").click()

        for key in self.form_dict.get("Home").keys():
            directory_span = self.page.query_selector(f"span:text('{key}')")
            assert directory_span

            directory_li = directory_span
            while directory_li and directory_li.evaluate('node => node.tagName.toLowerCase()') != "li":
                directory_li = directory_li.evaluate_handle('node => node.parentNode')
            assert directory_li.evaluate('node => node.tagName.toLowerCase()') == "li"

            self.__iterate_checkboxes(key, directory_li)

            time.sleep(5)

    def __iterate_checkboxes(self, key: str, directory_li, elements: list| dict = None):
        if not elements:
            elements = self.form_dict.get("Home").get(key)
        if type(elements) == list:
            if "All" in elements:
                directory_to_click = directory_li.query_selector(f"span.rct-title:has-text('{key}')")
                assert directory_to_click
                directory_to_click.click()

                checked_files = directory_li.query_selector_all(f"span.rct-title")
                for checked_file in checked_files:
                    if '.' in checked_file.inner_text():
                        base_name_file = checked_file.inner_text().rsplit('.', 1)[0]
                    else:
                        base_name_file = checked_file.inner_text()

                    base_name_file = base_name_file.replace(" ", "").lower()
                    self.checked.append(base_name_file)

                return

            for file in elements:
                file = directory_li.query_selector(f"span.rct-title:has-text('{file}')")
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
                sub_directory_li = self.page.query_selector(f"span.rct-title:has-text('{key}')")
                print(key, type(sub_directory_li))
                while sub_directory_li and sub_directory_li.evaluate("node => node.tagName.toLowerCase()") != "li":
                    sub_directory_li = sub_directory_li.evaluate_handle("node => node.parentNode")
                assert directory_li.evaluate('node => node.tagName.toLowerCase()') == "li"

                sub_elements = elements.get(sub_key)
                self.__iterate_checkboxes(sub_key, sub_directory_li, sub_elements)

    def __test_checkboxes(self):

        elements = self.page.query_selector_all("span.text-success")
        for element in elements:
            assert element.inner_text() in self.checked

    def __press_radio_button(self):
        key = list(self.form_dict.keys())[0]
        value = self.form_dict.get(key)
        interest_area = self.page.query_selector(f"div:has-text('{key}')")
        interest_area.evaluate("node => node.parentElement")
        interest_area.query_selector(f"label:has-text('{value}')").click()

    def __test_radio_button(self):
        key = list(self.form_dict.keys())[0]
        result = self.page.query_selector(".text-success").inner_text()
        assert result == self.form_dict.get(key)

    def __clear_table(self):
        delete_button = self.page.query_selector("span[title='Delete']")
        while delete_button:
            delete_button.click()
            delete_button = self.page.query_selector("span[title='Delete']")

    def __add_elements(self, to_be_added: list):
        for element in to_be_added:
            self.page.locator("#addNewRecordButton").click()
            complete_form = CompleteForm(form_dict=element, page = self.page)
            complete_form.find_type_and_action()
            self.page.locator("#submit").click()

    def __get_all_elements(self) -> list:
        elements = []
        columns = self.__get_all_columns()

        rows = self.page.query_selector_all("div.rt-tr-group")
        for row in rows:
            new_element = {}
            cells = row.query_selector_all("div")[:6]

            if cells[0].inner_text() == "":
                break
            else:
                print(cells[0].inner_text() ,type(cells[0].inner_text()))

            for (cell, column) in zip(cells, columns):
                new_element[column]= cell.inner_text()

            elements.append(new_element)

        return elements

    def __get_all_columns(self) -> list:
        return ["First Name", "Last Name", "Age", "Email", "Salary", "Department"]

    def __test_add_elements(self):
        pass

    def __edit_element(self):
        pass

    def __delete_elements(self, to_be_deleted: list[dict]):
        search_box = self.page.query_selector("#searchBox")

        for element in to_be_deleted:
            search_box.fill('')
            search_box.fill(element.get("Email"))
            rows =  self.page.query_selector_all("div.rt-tr-group")

            for row in rows:
                cells = row.query_selector_all("div")[:2]
                if cells[0].inner_text() == element.get("First Name") and cells[1].inner_text() == element.get("Last Name"):
                    delete_button = row.query_selector("span[title='Delete']")
                    delete_button.click()

