from datetime import datetime
from django.test import TestCase
from django.utils.timezone import localtime

from company.models import Account, Company
from road.models import Road
from road.serializers import OutputRoadSerializer


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

    def test_success_case(self):
        response_data = OutputRoadSerializer(self.road).data

        self.assertEqual(response_data["oid"], str(self.road.oid))
        self.assertEqual(response_data["name"], self.road.name)
        self.assertEqual(response_data["locations"], self.road.locations)
        self.assertEqual(response_data["created_at"], localtime(
            self.road.created_at,
        ).strftime("%d.%m.%Y %H:%M:%S"))

    def test_wrong_case(self):
        for data in self.invalid_road_data:
            with self.assertRaises(Exception):
                OutputRoadSerializer(data=data).data
