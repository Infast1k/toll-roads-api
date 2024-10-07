from rest_framework import status
from rest_framework.test import APITestCase

from company.commands import AuthTokens, LoginCommand, LoginCommandHandler
from company.models import Account


class RefreshViewTest(APITestCase):
    def setUp(self):
        self.url = "/api/v1/auth/refresh/"

        self.account = Account.objects.create(
            email="ZTqZ5@example.com",
            password="password",
        )

        self.login_command = LoginCommand(
            email=self.account.email,
            password=self.account.password,
        )

        self.tokens: AuthTokens = LoginCommandHandler.handle(
            command=self.login_command,
        )

        self.valid_input_data = {
            "refresh_token": self.tokens.refresh_token,
        }

        self.invalid_input_data = {
            "refresh_token": "invalid",
        }

    def test_success_refresh_view(self):
        response = self.client.post(self.url, data=self.valid_input_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access_token"))
        self.assertIsNotNone(response.data.get("refresh_token"))

        new_tokens: AuthTokens = AuthTokens(
            access_token=response.data.get("access_token"),
            refresh_token=response.data.get("refresh_token"),
        )

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
