from playwright.async_api import Page
from web_tables import WebTable
from navigator import navigate

def test_web_table(page: Page) -> None:

    form_dict = {
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
        ],
        "Edit":
        [
            {
            "First Name": "Test2",
            "Last Name": "Test",
            "Email": "test2@test.co",

            "New-Salary": "150000"
            }
        ]

    }

    destination = "Elements>Web Tables"
    page = navigate(page, destination)

    web_table_test = WebTable(form_dict = form_dict, page = page)
    web_table_test.test()