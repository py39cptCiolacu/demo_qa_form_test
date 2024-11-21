from playwright.sync_api import Page

class ElementInteractor:

    def __init__(self, base_url: str, page: Page)-> None:
        self.base_url = base_url
        self.page =  page

    def fill_textbox(self, sub_directory:str, locator: str, value: str) -> str:
        self.page.goto(self.base_url + sub_directory)
        self.page.locator(locator).fill(value)
        filled_value = self.page.locator(locator).input_value()

        return filled_value
