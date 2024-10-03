import jwt
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase

from company.commands import AuthTokens, LoginCommand, LoginCommandHandler
from company.models import Account


class LoginCommandTests(TestCase):
    def setUp(self):
        self.valid_input_data = {
            "email": "test@a.com",
            "password": "password",
        }

        self.invalid_input_data = [
            {
                "email": "test@b.com",
                "password": "password",
            },
            {
                "password": "password",
            },
            {
                "email": True,
                "password": "password",
            },
            {
                "email": "",
                "password": "password",
            },
        ]

        self.account = Account.objects.create(
            email=self.valid_input_data.get("email"),
            password=self.valid_input_data.get("password"),
        )

    def test_success_login_command(self):
        command = LoginCommand(
            email=self.valid_input_data.get("email"),
            password=self.valid_input_data.get("password"),
        )

        result: AuthTokens = LoginCommandHandler.handle(command=command)
        refresh = cache.get(key=str(result.refresh_token))

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.access_token)
        self.assertIsNotNone(result.refresh_token)

        self.assertIsNotNone(refresh)

        decoded_jwt = jwt.decode(
            jwt=result.access_token,
            key=settings.JWT_SECRET,
            algorithms=["HS256"],
        )

        self.assertEqual(str(self.account.oid), decoded_jwt.get("sub"))

    def test_fail_login_command(self):
        wrong_commands = []

        for data in self.invalid_input_data:
            wrong_commands.append(
                LoginCommand(
                    email=data.get("email"),
                    password=data.get("password"),
                )
            )

        for command in wrong_commands:
            with self.assertRaises(Exception):
                LoginCommandHandler.handle(command=command)
