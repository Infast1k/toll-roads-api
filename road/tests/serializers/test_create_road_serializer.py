from django.test import TransactionTestCase
from rest_framework import serializers

from company.models import Account, Company
from road.serializers import InputCreateRoadSerializer


class InputCreateRoadSerializerTest(TransactionTestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email="testemail@mail.ru",
            password="testpassword",
        )

        self.company = Company.objects.create(
            name="Test Company",
            account=self.account,
        )

        self.valid_input_data = {
            "road_name": "test road name",
            "road_locations": "test road locations",
            "company_name": self.company.name,
        }

        self.invalid_input_data = [
            {
                "road_name": "other test road name",
                "road_locations": "other test road locations",
                "company_name": "some company name",
            },
            {
                "road_name": "other test road name",
                "road_location": "test road location",
                "company_name": self.company.name,
            },
            {
                "road_name": "test road name",
                "road_location": "other test road location",
                "company_name": self.company.name,
            },
            {
                "road_name": "test road name",
                "road_locations": "other test road locations",
            },
            {
                "road_name": "test road name",
                "company_name": self.company.name,
            },
            {
                "road_locations": "test road locations",
            },
            {}
        ]

    def test_valid_input(self):
        response = InputCreateRoadSerializer(data=self.valid_input_data)
        response.is_valid(raise_exception=True)

    def test_wrong_input(self):
        for data in self.invalid_input_data:
            with self.assertRaises(serializers.ValidationError):
                response = InputCreateRoadSerializer(data=data)
                response.is_valid(raise_exception=True)
