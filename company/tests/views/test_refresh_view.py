from rest_framework import status
from rest_framework.test import APITestCase

from company.models import Account
from company.services import JWTService


class RefreshViewTest(APITestCase):
    def setUp(self):
        self.url = "/api/v1/auth/refresh/"

        self.account = Account.objects.create(
            email="ZTqZ5@example.com",
            password="password",
        )

        self.tokens = JWTService.generate_tokens(account_oid=self.account.oid)

        self.valid_input_data = {
            "refresh_token": self.tokens.get("refresh_token"),
        }

        self.invalid_input_data = {
            "refresh_token": "invalid",
        }

    def test_success_refresh_view(self):
        response = self.client.post(self.url, data=self.valid_input_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access_token"))
        self.assertIsNotNone(response.data.get("refresh_token"))

        new_tokens = {
            "access_token": response.data.get("access_token"),
            "refresh_token": response.data.get("refresh_token"),
        }

        self.assertNotEqual(
            self.tokens,
            new_tokens,
        )

    def test_fail_refresh_view(self):
        response = self.client.post(self.url, data=self.invalid_input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.post(self.url, data=self.valid_input_data)
        response = self.client.post(self.url, data=self.invalid_input_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
