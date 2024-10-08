from uuid import uuid4
from django.test import TransactionTestCase
from rest_framework import serializers

from company.models import Account, Company
from road.models import Road
from road.serializers import InputDeleteRoadSerializer


class DeleteRoadSerializerTest(TransactionTestCase):
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
            },
            {
                "company_name": self.company.name,
            },
            {
                "road_oid": self.road.oid,
                "company_name": "some company name",
            },
            {
                "road_oid": uuid4(),
                "company_name": self.company.name,
            },
        ]

    def test_valid_input(self):
        response = InputDeleteRoadSerializer(data={
            "road_oid": self.road.oid,
            "company_name": self.company.name,
        })

        response.is_valid(raise_exception=True)

    def test_wrong_input(self):
        for data in self.invalid_input_data:
            with self.assertRaises(serializers.ValidationError):
                response = InputDeleteRoadSerializer(data=data)
                response.is_valid(raise_exception=True)
