from uuid import uuid4
from django.test import TestCase

from company.models import Account, Company
from road.commands import UpdateRoadCommand, UpdateRoadCommandHandler
from road.models import Road


class UpdateRoadCommandHandlerTest(TestCase):
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
        commands: list[UpdateRoadCommand] = []

        for data in self.valid_input_data:
            commands.append(
                UpdateRoadCommand(
                    road_oid=data.get("road_oid"),
                    name=data.get("road_name"),
                    locations=data.get("road_locations"),
                    company_name=data.get("company_name"),
                )
            )

        for command in commands:
            result: Road = UpdateRoadCommandHandler.handle(command=command)

            self.assertEqual(result.oid, command.road_oid)
            self.assertEqual(result.company.name, command.company_name)

            if command.name is not None:
                self.assertEqual(result.name, command.name)
            if command.locations is not None:
                self.assertEqual(result.locations, command.locations)

    def test_invalid_case(self):
        wrong_commands = []

        for data in self.invalid_input_data:
            wrong_commands.append(
                UpdateRoadCommand(
                    road_oid=data.get("road_oid"),
                    name=data.get("road_name"),
                    locations=data.get("road_locations"),
                    company_name=data.get("company_name"),
                )
            )

        for command in wrong_commands:
            with self.assertRaises(Road.DoesNotExist):
                UpdateRoadCommandHandler.handle(command=command)
