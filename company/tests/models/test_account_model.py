from django.db.utils import IntegrityError
from django.test import TestCase

from company.models import Account


class AccountModelTests(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email="infast1k@mail.ru",
            password="testpassword",
        )

    def test_account_str(self):
        self.assertEqual(str(self.account), "infast1k@mail.ru")

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            Account.objects.create(
                email="infast1k@mail.ru",
                password="testpassword",
            )
