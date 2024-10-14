from django.db import IntegrityError
from django.test import TransactionTestCase

from company.models import Account
from company.services import AccountService


class AccountServiceTest(TransactionTestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email="testemail@mail.ru",
            password="testpassword",
        )

    def test_success_create_account(self):
        AccountService.create_account(
            email="testemail2@mail.ru",
            password="testpassword",
        )

        self.assertEqual(Account.objects.count(), 2)

    def test_wrong_create_account(self):
        with self.assertRaises(IntegrityError):
            AccountService.create_account(
                email="testemail@mail.ru",
                password="testpassword",
            )

        self.assertEqual(Account.objects.count(), 1)

    def test_success_get_account_by_email(self):
        account = AccountService.get_account_by_email("testemail@mail.ru")

        self.assertIsNotNone(account)
        self.assertEqual(account, self.account)

    def test_wrong_get_account_by_email(self):
        with self.assertRaises(Account.DoesNotExist):
            AccountService.get_account_by_email("testemail2@mail.ru")
