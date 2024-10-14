from uuid import uuid4
from django.core.cache import cache
from django.test import TestCase

from company.models import Account
from company.services import JWTService


class JWTServiceTest(TestCase):
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

    def test_success_generate_tokens(self):
        tokens = JWTService.generate_tokens(account_oid=self.account)

        self.assertIsNotNone(tokens)
        self.assertIsNotNone(tokens.get("access_token"))
        self.assertIsNotNone(tokens.get("refresh_token"))
        self.assertIsNotNone(cache.get(key=str(tokens.get("refresh_token"))))

    def test_success_refresh_tokens(self):
        tokens = JWTService.generate_tokens(account_oid=self.account)

        new_tokens = JWTService.refresh_tokens(
            refresh_token=tokens.get("refresh_token"),
        )

        self.assertIsNotNone(
            cache.get(
                key=str(new_tokens.get("refresh_token")),
            )
        )
        self.assertNotEqual(tokens, new_tokens)

    def test_wrong_refresh_tokens(self):
        tokens = JWTService.generate_tokens(account_oid=self.account)

        cache.delete(key=str(tokens.get("refresh_token")))

        with self.assertRaises(ValueError):
            JWTService.refresh_tokens(
                refresh_token=tokens.get("refresh_token"),
            )

        with self.assertRaises(ValueError):
            JWTService.refresh_tokens(
                refresh_token=uuid4(),
            )
