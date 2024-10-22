from datetime import datetime
from django.test import TestCase
from django.utils.timezone import localtime

from company.models import Account, Company
from road.models import Road
from road.serializers import OutputRoadsWithPaginationSerializer


class OutputRoadSerializerTest(TestCase):
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

        self.invalid_road_data = [
            {
                "name": "Test Road",
                "locations": "Test Locations",
                "company": "Invalid Company",
            },
            {
                "name": "Test Road",
                "locations": "Test Locations",
            },
            {
                "locations": "Test Locations",
                "created_at": datetime.now(),
            },
            {
                "name": "Test Road",
                "locations": "Test Locations",
                "created_at": datetime.now(),
            }
        ]

    def test_success_case(self) -> None:
        response_data = OutputRoadsWithPaginationSerializer({
            "roads": [self.road],
            "total": 1,
        }).data

        self.assertEqual(response_data.get("roads")[0]["oid"], str(self.road.oid))
        self.assertEqual(response_data.get("roads")[0]["name"], self.road.name)
        self.assertEqual(response_data.get("roads")[0]["locations"], self.road.locations)
        self.assertEqual(response_data.get("roads")[0]["created_at"], localtime(
            self.road.created_at,
        ).strftime("%d.%m.%Y %H:%M:%S"))

        self.assertEqual(response_data.get("total"), 1)

    def test_wrong_case(self):
        for data in self.invalid_road_data:
            with self.assertRaises(Exception):
                OutputRoadsWithPaginationSerializer(data=data).data
