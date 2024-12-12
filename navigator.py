from playwright.sync_api import Page

URL = "https://demoqa.com/"

def navigate(page: Page, destination: str) -> Page:

    page.goto(URL)

    destination_as_list = destination.split(">")
    page.locator(f"h5:text(\"{destination_as_list[0]}\")").click()
    page.locator(f"span:text(\"{destination_as_list[1]}\")").click()
    return page