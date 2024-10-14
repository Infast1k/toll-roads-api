from django.db import IntegrityError
from django.test import TransactionTestCase

from company.models import Account, Company
from company.services import CompanyService


class CompanyServiceTest(TransactionTestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email="testemail@mail.ru",
            password="testpassword",
        )
        self.company = Company.objects.create(
            name="Test Company",
            account=self.account,
        )

    def test_success_create_company(self):
        account = Account.objects.create(
            email="testemail2@mail.ru",
            password="testpassword",
        )
        company = CompanyService.create_company(
            company_name="New Company Name",
            account=account,
        )

        self.assertIsNotNone(company)
        self.assertNotEqual(company, self.company)
        self.assertEqual(company.account, account)
        self.assertEqual(company.name, "New Company Name")

    def test_wrong_create_company(self):
        with self.assertRaises(IntegrityError):
            CompanyService.create_company(
                company_name="New Company Name",
                account=self.account,
            )

        with self.assertRaises(IntegrityError):
            CompanyService.create_company(
                company_name="Test Company",
                account=self.account,
            )

        self.assertEqual(Company.objects.count(), 1)
