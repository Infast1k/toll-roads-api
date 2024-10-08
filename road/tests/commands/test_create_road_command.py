from django.test import TestCase

from company.models import Account, Company
from road.commands import CreateRoadCommand, CreateRoadCommandHandler
from road.models import Road


class CreateRoadCommandHandlerTest(TestCase):
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
                "road_locations": "test road locations",
                "company_name": "some company name",
            },
        ]

    def test_valid_case(self):
        command = CreateRoadCommand(
            road_name=self.valid_input_data.get("road_name"),
            road_locations=self.valid_input_data.get("road_locations"),
            company_name=self.valid_input_data.get("company_name"),
        )

        result = CreateRoadCommandHandler.handle(command=command)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, self.valid_input_data.get("road_name"))
        self.assertEqual(
            result.locations,
            self.valid_input_data.get("road_locations"),
        )
        self.assertEqual(result.company, self.company)

    def test_invalid_case(self):
        wrong_commands = []

        for data in self.invalid_input_data:
            wrong_commands.append(
                CreateRoadCommand(
                    road_name=data.get("road_name"),
                    road_locations=data.get("road_locations"),
                    company_name=data.get("company_name"),
                )
            )

        for command in wrong_commands:
            with self.assertRaises(Exception):
                CreateRoadCommandHandler.handle(command=command)
