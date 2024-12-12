from playwright.async_api import Page
from individuial_elements import IndividualElements

from navigator import navigate

def test_check_box(page: Page) -> None:
    form_dict = {
        "Home": {
            "Desktop" : ["Notes"],
            "Documents": {
                "WorkSpace": ["All"],
                "Office": ["Private", "General"]
            },
        }
    }

    page = navigate(page, "Elements>Check Box")
    check_box_test = IndividualElements(form_dict=form_dict, page=page, type="Check Box")
    check_box_test.test()