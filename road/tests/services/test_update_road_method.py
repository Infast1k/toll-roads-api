from uuid import uuid4
from django.test import TestCase

from company.models import Account, Company
from road.models import Road
from road.services import RoadService


class UpdateRoadServiceMethodTest(TestCase):
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

        self.valid_input_data = [
            {
                "road_oid": self.road.oid,
                "road_name": "new test road name",
                "road_locations": "new test road locations",
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "road_locations": "new test road locations",
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "road_name": "new test road name",
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "company_name": self.company.name,
            },
        ]

        self.invalid_input_data = [
            {
                "road_oid": uuid4(),
                "road_name": "new test road name",
                "road_locations": "new test road locations",
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "road_name": "new test road name",
                "road_locations": "new test road locations",
                "company_name": "some company name",
            },
            {
                "road_oid": self.road.oid,
                "road_name": "new test road name",
                "road_locations": "new test road locations",
            },
            {
                "road_name": "new test road name",
                "road_locations": "new test road locations",
                "company_name": self.company.name,
            },
            {},
        ]

    def test_valid_case(self):
        for case in self.valid_input_data:
            result = RoadService.update_road(
                road_oid=case.get("road_oid"),
                road_name=case.get("road_name"),
                road_locations=case.get("road_locations"),
                company_name=case.get("company_name"),
            )

            self.assertEqual(result.oid, case.get("road_oid"))
            self.assertEqual(result.company.name, case.get("company_name"))

            if case.get("road_name") is not None:
                self.assertEqual(result.name, case.get("road_name"))
            if case.get("road_locations") is not None:
                self.assertEqual(result.locations, case.get("road_locations"))

    def test_invalid_case(self):
        for case in self.invalid_input_data:
            with self.assertRaises(Road.DoesNotExist):
                RoadService.update_road(
                    road_oid=case.get("road_oid"),
                    road_name=case.get("road_name"),
                    road_locations=case.get("road_locations"),
                    company_name=case.get("company_name"),
                )
