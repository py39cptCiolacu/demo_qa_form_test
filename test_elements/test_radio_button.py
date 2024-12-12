from playwright.sync_api import Page

from individuial_elements import IndividualElements
from navigator import navigate

def test_radio_button(page: Page) -> None:

    form_dict = {
        "Do you like the site?" : "Yes"
    }

    page = navigate(page, "Elements>Radio Button")
    radio_button_test = IndividualElements(form_dict=form_dict, page=page, type = "Radio Button")
    radio_button_test.test()

