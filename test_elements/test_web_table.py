from playwright.async_api import Page

from individuial_elements import IndividualElements

def test_web_table(page: Page) -> None:

    form_dict = {
        "destination": "Elements>Web Tables",
        "Add":
        [
            {
             "First Name": "Test",
             "Last Name": "Test",
             "Email": "test@test.co",
             "Age": "22",
             "Salary": "120000",
             "Department": "IT"
            },
            {
            "First Name": "Test2",
            "Last Name": "Test",
            "Email": "test2@test.co",
            "Age": "22",
            "Salary": "120000",
            "Department": "IT"
            }
        ],
        "Delete":
        [
            {
            "First Name": "Test",
            "Last Name": "Test",
            "Email": "test@test.co"
            }
        ]
    }

    web_table_test = IndividualElements(form_dict = form_dict, page = page)
    web_table_test.test()