from playwright.sync_api import Page

class ElementGetter:
   def __init__(self, page: Page) -> None:
      self.page = page

   def get_input_text(self, locator: str) -> str:
      text_value = self.page.locator(locator).input_value()
      return text_value
   
   def get_content_text(self, locator: str) -> str:
      text_value = self.page.locator(locator).text_content()
      return text_value

   def get_checkbox_status(self, locator: str) -> bool:
      checkbox_value = self.page.locator(locator).is_checked()
      return checkbox_value