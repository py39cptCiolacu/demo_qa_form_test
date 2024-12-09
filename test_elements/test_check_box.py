from playwright.async_api import Page
from individuial_elements import IndividualElements

def test_check_box(page: Page) -> None:
    form_dict = {
        "destination": "Elements>Check Box",
        "Home": {
            "Desktop" : ["Notes"],
            "Documents": {
                "WorkSpace": ["All"],
                "Office": ["Private", "General"]
            },
        }
    }

    check_box_test = IndividualElements(form_dict=form_dict, page=page)
    check_box_test.test()