from playwright.async_api import Page

from element_interactor import ElementInteractor
from element_getter import ElementGetter

URL = "https://demoqa.com/checkbox"


def test_home_checkbox_status(
    page: Page, element_interactor: ElementInteractor, element_getter: ElementGetter
):
    page.goto(URL)
    locator = "label[for='tree-node-home'] .rct-checkbox"
    element_interactor.press_on_box(locator)
    assert element_getter.get_checkbox_status(locator)


def test_desktop_checkbox(
    page: Page, element_interactor: ElementInteractor, element_getter: ElementGetter
):
    page.goto(URL)
    tree_expander_locator = ".rct-collapse.rct-collapse-btn"
    desktop_checkbox_locator = "label[for='tree-node-desktop'] .rct-checkbox"

    element_interactor.click_on_button(tree_expander_locator)
    element_interactor.press_on_box(desktop_checkbox_locator)

    assert element_getter.get_checkbox_status(desktop_checkbox_locator)
