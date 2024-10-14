from django.test import TestCase

from company.models import Account, Company
from road.models import Road
from road.services import RoadService


class GetAllRoadsServiceMethodTest(TestCase):
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

    def test_success_case(self):
        result = RoadService.get_roads_by_company_name(
            company_name=self.company.name,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.road)

    def test_invalid_case(self):
        result = RoadService.get_roads_by_company_name(
            company_name="does not exists company name",
        )

        self.assertEqual(len(result), 0)
