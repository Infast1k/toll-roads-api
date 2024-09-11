from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase

from company.models import Account


class LoginViewTest(APITestCase):
    def setUp(self):
        self.url = "/api/v1/sign-in/"

        self.valid_data = {
            "email": "ZTqZ5@example.com",
            "password": "password",
        }

        self.invalid_data = [
            {
                "email": self.valid_data.get("email"),
                "password": "wrong_password",
            },
            {
                "email": "wrong_email",
                "password": self.valid_data.get("password"),
            },
            {
                "email": "wrong_email",
                "password": "wrong_password",
            },
            {
                "password": self.valid_data.get("password"),
            },
            {
                "email": self.valid_data.get("email"),
            },
            {
                "email": True,
                "password": "wrong_password",
            },
            {
                "email": "wrong_email",
                "password": True,
            },
            {
                "email": True,
                "password": True,
            },
            {},
        ]

        Account.objects.create(
            email=self.valid_data.get("email"),
            password=make_password(self.valid_data.get("password")),
        )

    def test_successfully_register_view(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access_token"))
        self.assertIsNotNone(response.data.get("refresh_token"))

    def test_unsuccessfully_register_view(self):
        for data in self.invalid_data:
            response = self.client.post(
                self.url,
                data,
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
