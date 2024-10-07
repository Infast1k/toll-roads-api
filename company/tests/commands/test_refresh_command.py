from django.test import TestCase

from company.commands import (
    AuthTokens,
    LoginCommand,
    LoginCommandHandler,
    RefreshCommand,
    RefreshCommandHandler,
)
from company.models import Account


class RefreshCommandTests(TestCase):
    def setUp(self):
        self.input_data = {
            "email": "test@a.com",
            "password": "password",
        }

        Account.objects.create(
            email=self.input_data.get("email"),
            password=self.input_data.get("password"),
        )

        self.login_command = LoginCommand(
            email=self.input_data.get("email"),
            password=self.input_data.get("password"),
        )

        self.tokens: AuthTokens = LoginCommandHandler.handle(
            command=self.login_command,
        )

    def test_success_refresh_command(self):
        refresh_command = RefreshCommand(
            refresh_token=self.tokens.refresh_token,
        )

        new_tokens: AuthTokens = RefreshCommandHandler.handle(
            command=refresh_command,
        )

        self.assertNotEqual(
            self.tokens,
            new_tokens,
        )

    def test_fail_refresh_command(self):
        refresh_command = RefreshCommand(
            refresh_token=self.tokens.refresh_token,
        )

        RefreshCommandHandler.handle(command=refresh_command)

        with self.assertRaises(ValueError):
            RefreshCommandHandler.handle(command=refresh_command)
