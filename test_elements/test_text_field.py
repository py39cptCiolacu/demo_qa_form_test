from playwright.async_api import Page

from complete_form import CompleteForm


def test_text_form(page: Page) -> None:

    test_dict = {
                 "destination": "Elements>Text Box",
                 "Full Name": "Test test",
                 "Email": "test@test.com",
                 "Current Address": "Str. Test. Test",
                 "Permanent Address": "Str. Test. Test",
                 }

    complete_form = CompleteForm(test_dict, page)
    complete_form.test()
