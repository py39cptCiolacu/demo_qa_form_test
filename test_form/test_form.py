from playwright.sync_api import Page
from complete_form import CompleteForm

from navigator import navigate

def test_form(page: Page) -> None:
    form_dict = {
        "Name": ["Test", "Test"],
        "Email": "test@test.co",
        "Gender" : "Male",
        "Mobile": "1111111111",
        "Date of Birth": "05 November,2001",
        "Subjects": "Maths",
        "Hobbies": ["Sports", "Music"],
        "Current Address": "Str. Test nr 12",
        "State and City": ["NCR", "Delhi"]
    }

    page = navigate(page,"Forms>Practice Form")
    complete_form_test = CompleteForm(form_dict=form_dict, page=page, test_with_modal=True)
    complete_form_test.test()