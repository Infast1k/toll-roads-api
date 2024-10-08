from django.db import IntegrityError
from django.test import TransactionTestCase

from company.models import Account, Company
from road.models import Road


class RoadModelTest(TransactionTestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email="testemail@mail.ru",
            password="testpassword",
        )

        self.company = Company.objects.create(
            name="Test Company",
            account=self.account,
        )

        self.road = Road.objects.create(
            name="Test Road",
            locations="Test Locations",
            company=self.company,
        )

    def test_model_to_str(self):
        self.assertEqual(str(self.road), "Test Road - Test Company")

    def test_model_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            Road.objects.create(
                name=self.road.name,
                locations="new location",
                company=self.company,
            )

        with self.assertRaises(IntegrityError):
            Road.objects.create(
                name="new name",
                locations=self.road.locations,
                company=self.company,
            )

        self.assertEqual(Road.objects.all().count(), 1)

    def test_company_foreign_key(self):
        self.assertEqual(self.road.company, self.company)
