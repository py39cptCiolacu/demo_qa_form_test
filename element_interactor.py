from playwright.sync_api import Page


class ElementInteractor:
    def __init__(self, page: Page) -> None:
        self.page = page

    def fill_textbox(self, locator: str, value: str):
        self.page.locator(locator).fill(value)

    def press_on_box(self, locator: str, index: int = 0) -> None:
        self.page.locator(locator).nth(index).check()

    def click_on_button(self, locator: str, index: int = 0) -> None:
        self.page.locator(locator).nth(index).click()