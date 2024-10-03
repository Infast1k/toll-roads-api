from django.db.utils import IntegrityError
from django.test import TestCase

from company.commands import (
    RegisterCompanyCommand,
    RegisterCompanyCommandHandler,
)
from company.models import Account, Company


class RegisterCommandTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Company",
            "email": "YwqFP@example.com",
            "password": "testpassword",
        }

        self.invalid_data = {
            "name": "Test Company",
            "email": "otherYwqFP@example.com",
            "password": "testpassword",
        }

    def test_successfully_register_command(self):
        command = RegisterCompanyCommand(
            name=self.valid_data.get("name"),
            email=self.valid_data.get("email"),
            password=self.valid_data.get("password"),
        )

        company = RegisterCompanyCommandHandler.handle(command)

        self.assertIsNotNone(company)
        self.assertIsNotNone(company.account)

        self.assertEqual(company.name, self.valid_data.get("name"))
        self.assertEqual(company.account.email, self.valid_data.get("email"))
        self.assertTrue(company.account.check_password(
            self.valid_data.get("password")
        ))

    def test_unsuccessfully_register_command(self):
        command = RegisterCompanyCommand(
            name=self.valid_data.get("name"),
            email=self.valid_data.get("email"),
            password=self.valid_data.get("password"),
        )
        RegisterCompanyCommandHandler.handle(command)

        command = RegisterCompanyCommand(
            name=self.invalid_data.get("name"),
            email=self.invalid_data.get("email"),
            password=self.invalid_data.get("password"),
        )

        with self.assertRaises(IntegrityError):
            RegisterCompanyCommandHandler.handle(command)

        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)

        self.assertIsNone(
            Account.objects.filter(
                email=self.invalid_data.get("email"),
            ).first()
        )
