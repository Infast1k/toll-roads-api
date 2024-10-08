from uuid import uuid4
from django.test import TransactionTestCase
from rest_framework import serializers

from company.models import Account, Company
from road.models import Road
from road.serializers import InputUpdateRoadSerializer


class InputUpdateRoadSerializerTest(TransactionTestCase):
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
                "name": "new road name",
                "locations": "new road locations",
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "name": None,
                "locations": "new road locations",
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "name": "new road name",
                "locations": None,
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "name": None,
                "locations": None,
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "name": self.road.name,
                "locations": self.road.locations,
                "company_name": self.company.name,
            },
        ]

        self.invalid_input_data = [
            {
                "road_oid": self.road.oid,
                "name": "other new road name",
                "locations": "other new road locations",
                "company_name": "some company name",
            },
            {
                "road_oid": uuid4(),
                "name": "new road name",
                "locations": "new road locations",
                "company_name": "some company name",
            },
            {
                "name": "new road name",
                "locations": "new road locations",
                "company_name": "some company name",
            },
            {
                "road_oid": self.road.oid,
                "locations": "new road locations",
                "company_name": "some company name",
            },
            {
                "road_oid": self.road.oid,
                "name": "new road name",
                "company_name": "some company name",
            },
            {},
        ]

    def test_valid_input(self):
        for data in self.valid_input_data:
            response = InputUpdateRoadSerializer(data=data)
            response.is_valid(raise_exception=True)

    def test_wrong_input(self):
        for data in self.invalid_input_data:
            with self.assertRaises(serializers.ValidationError):
                response = InputUpdateRoadSerializer(data=data)
                response.is_valid(raise_exception=True)
