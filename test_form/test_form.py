from playwright.async_api import Page
from complete_form import CompleteForm

def test_form(page: Page) -> None:
    form_dict = {
        "destination": "Forms>Practice Form",
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

    complete_form_test = CompleteForm(form_dict=form_dict, page=page, test_with_modal=True)
    complete_form_test.test()