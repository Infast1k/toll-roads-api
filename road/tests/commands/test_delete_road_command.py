from uuid import uuid4
from django.test import TestCase

from company.models import Account, Company
from road.commands import DeleteRoadByOidCommand, DeleteRoadByOidCommandHandler
from road.models import Road


class DeleteRoadByOidCommandHandlerTest(TestCase):
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
        command = DeleteRoadByOidCommand(
            road_oid=self.road.oid,
            company_name=self.company.name,
        )

        result = DeleteRoadByOidCommandHandler.handle(command=command)

        self.assertIsNone(result)
        self.assertEqual(
            Company.objects.get(name=self.company.name).roads.count(), 0
        )
        self.assertEqual(Road.objects.count(), 0)

    def test_invalid_case(self):
        wrong_commands = []

        for data in self.invalid_input_data:
            wrong_commands.append(
                DeleteRoadByOidCommand(
                    road_oid=data.get("road_oid"),
                    company_name=data.get("company_name"),
                )
            )

        for command in wrong_commands:
            with self.assertRaises(Exception):
                DeleteRoadByOidCommandHandler.handle(command=command)

        self.assertEqual(Road.objects.count(), 1)
