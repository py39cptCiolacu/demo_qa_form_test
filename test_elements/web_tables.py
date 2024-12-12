import time

from playwright.sync_api import Page, ElementHandle
from complete_form import CompleteForm


class WebTable:
    def __init__(self, form_dict: dict, page: Page) -> None:
        self.form_dict = form_dict
        self.page = page

    def test(self):
        if "Add" in self.form_dict.keys():
            self.__add_elements(self.form_dict.get("Add"))
            self.__test_add_elements(self.form_dict.get("Add"))
        if "Delete" in self.form_dict.keys():
            self.__delete_elements(self.form_dict.get("Delete"))
            self.__test_delete_elements(self.form_dict.get("Delete"))
        if "Edit" in self.form_dict.keys():
            print(self.__get_all_elements())
            for element in self.form_dict.get("Edit"):
                element_row_before = self.__find_element_row(element)
                element_dict_before = self.__element_row_to_dict(element_row_before)

                self.__edit_element(element)

                element_row_after = self.__find_element_row(element)
                element_dict_after = self.__element_row_to_dict(element_row_after)

                self.__test_edit_element(element_dict_before, element_dict_after, element)

    def __clear_table(self):
        delete_button = self.page.query_selector("span[title='Delete']")
        while delete_button:
            delete_button.click()
            delete_button = self.page.query_selector("span[title='Delete']")

    def __add_elements(self, to_be_added: list):
        for element in to_be_added:
            self.page.locator("#addNewRecordButton").click()
            complete_form = CompleteForm(form_dict=element, page=self.page)
            complete_form.find_type_and_take_action()
            self.page.locator("#submit").click()

    def __get_all_elements(self) -> list:
        elements = []
        columns = self.__get_all_columns()

        rows = self.page.locator("div.rt-tr-group").all()
        for row in rows:
            new_element = {}
            cells = row.locator("div[role='gridcell']").all()

            if cells[0].inner_text().replace("\xa0", "") == "":
                continue

            for (cell, column) in zip(cells, columns):
                new_element[column] = cell.inner_text()

            elements.append(new_element)

        return elements

    def __get_all_columns(self) -> list:

        table_head_elements = self.page.query_selector_all("div[role='columnheader']")
        columns = []
        for table_head_element in table_head_elements:
            columns.append(table_head_element.inner_text())

        if "Action" in columns:
            columns.remove("Action")

        return columns

    def __find_element_row(self, element: dict) -> ElementHandle | None:

        search_box = self.page.query_selector("#searchBox")
        search_box.fill('')
        search_box.fill(element.get('Email'))
        rows = self.page.query_selector_all("div[role='row']")

        for row in rows:
            cells = row.query_selector_all("div")[:2]
            if cells[0].inner_text().strip() == element.get("First Name") and cells[
                1].inner_text().strip() == element.get("Last Name"):
                return row

        return None

    def __element_row_to_dict(self, row: ElementHandle) -> dict:

        columns = self.__get_all_columns()
        cells = row.query_selector_all(".rt-td")[:6]
        element_dict = {}
        for cell, column in zip(cells, columns):
            element_dict[column] = cell.inner_text()

        return element_dict

    def __edit_element(self, element: dict):

        element_row = self.__find_element_row(element)
        assert element_row, "The element could not be found"
        edit_button = element_row.query_selector("span[title='Edit']")
        edit_button.click()

        fields_to_be_edited = {}

        for key in element.keys():
            if key.startswith("New-"):
                new_key = key.removeprefix("New-")
                fields_to_be_edited[new_key] = element[key]

        complete_form = CompleteForm(form_dict=fields_to_be_edited, page=self.page)
        complete_form.find_type_and_take_action()
        self.page.locator("#submit").click()

    def __delete_elements(self, to_be_deleted: list[dict]):

        for element in to_be_deleted:
            element_row = self.__find_element_row(element)
            assert element_row
            delete_button = element_row.query_selector("span[title='Delete']")
            delete_button.click()

    def __test_add_elements(self, elements: list[dict]) -> None:
        for element in elements:
            element_row = self.__find_element_row(element)
            assert element_row

    def __test_delete_elements(self, elements: list[dict]) -> None:
        for element in elements:
            element_row = self.__find_element_row(element)
            assert not element_row

    def __test_edit_element(self, element_dict_before: dict, element_dict_after: dict, element: dict) -> None:
        columns = self.__get_all_columns()
        should_be_changed = {}
        for key in element.keys():
            if key.startswith("New-"):
                new_key = key.removeprefix("New-")
                should_be_changed[new_key] = element.get(key)

        for column in columns:
            if column in should_be_changed:
                assert element_dict_after.get(column) == should_be_changed.get(column)
            else:
                assert element_dict_after.get(column) == element_dict_before.get(column)
