from django.db.utils import IntegrityError
from django.test import TestCase

from company.models import Account, Company


class CompanyModelTests(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email="infast1k@mail.ru",
            password="testpassword",
        )

        self.company = Company.objects.create(
            name="Test Company",
            account=self.account,
        )

    def test_company_str(self):
        self.assertEqual(str(self.company), "Test Company")

    def test_company_account(self):
        self.assertEqual(self.company.account, self.account)

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Company.objects.create(
                name=self.company.name,
                account=self.account,
            )

    def test_delete_cascade(self):
        self.account.delete()

        self.assertEqual(Company.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
