from playwright.async_api import Page

from individuial_elements import IndividualElements

def test_radio_button(page: Page) -> None:

    form_dict = {
        "destination" : "Elements>Radio Button",
        "Do you like the site?" : "Yes"
    }

    radio_button_test = IndividualElements(form_dict=form_dict, page=page)
    radio_button_test.test()

