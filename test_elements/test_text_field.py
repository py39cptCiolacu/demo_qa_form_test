from playwright.sync_api import Page

from complete_form import CompleteForm
from navigator import navigate


def test_text_form(page: Page) -> None:
    test_dict = {
        "Full Name": "Test test",
        "Email": "test@test.com",
        "Current Address": "Str. Test. Test",
        "Permanent Address": "Str. Test. Test",
    }

    page = navigate(page, "Elements>Text Box")
    complete_form = CompleteForm(test_dict, page)
    complete_form.test()
