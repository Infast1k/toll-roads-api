from rest_framework import status
from rest_framework.test import APITestCase


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.url = "/api/v1/auth/sign-up/"

        self.valid_data = {
            "name": "Company name",
            "account": {
                "email": "a@a.com",
                "password": "12345678",
            },
        }

        self.invalid_data = [
            {
                "name": "Company 2",
                "account": {
                    "email": "ZTqZ5@example.com",
                },
            },
            {
                "name": "Company 3",
                "account": {
                    "password": "password",
                },
            },
            {
                "name": "Company 4",
                "account": {},
            },
            {
                "name": "Company 5",
                "account": "account",
            },
            {
                "name": "Company 6",
                "account": {
                    "email": "ZTqZ5@example.com",
                    "password": "pasword",
                },
            },
            {
                "account": {
                    "email": "ZTqZ5@example.com",
                    "password": "pasword",
                }
            },
            {
                "name": True,
                "account": {
                    "email": "ZTqZ5@example.com",
                    "password": "password",
                },
            },
        ]

    def test_successfully_register_view(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.valid_data["name"])
        self.assertEqual(
            response.data["account"]["email"],
            self.valid_data["account"]["email"],
        )

    def test_unsuccessfully_register_view(self):
        for data in self.invalid_data:
            response = self.client.post(
                self.url,
                data,
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
