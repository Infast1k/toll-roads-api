from uuid import uuid4
from django.test import TestCase

from company.models import Account, Company
from road.models import Road
from road.services import RoadService


class DeleteRoadByOidServiceMethodTest(TestCase):
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

        self.invalid_input_data = [
            {
                "road_oid": self.road.oid,
                "company_name": "some company name",
            },
            {
                "road_oid": uuid4(),
                "company_name": self.company.name,
            }
        ]

    def test_valid_case(self):
        result = RoadService.delete_road_by_oid(
            road_oid=self.road.oid,
            company_name=self.company.name,
        )

        self.assertIsNone(result)
        self.assertEqual(
            Company.objects.get(name=self.company.name).roads.count(), 0
        )
        self.assertEqual(Road.objects.count(), 0)

    def test_invalid_case(self):
        for case in self.invalid_input_data:
            with self.assertRaises(Road.DoesNotExist):
                RoadService.delete_road_by_oid(
                    road_oid=case.get("road_oid"),
                    company_name=case.get("company_name"),
                )

        self.assertEqual(Road.objects.count(), 1)
