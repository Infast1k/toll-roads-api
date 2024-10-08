from django.test import TestCase

from company.models import Account, Company
from road.commands import GetAllRoadsCommand, GetAllRoadsCommandHandler
from road.models import Road


class GetAllRoadsCommandHandlerTest(TestCase):
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

    def test_success_case(self):
        command = GetAllRoadsCommand(company_name=self.company.name)
        result = GetAllRoadsCommandHandler.handle(command=command)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.road)

    def test_invalid_case(self):
        command = GetAllRoadsCommand(
            company_name="does not exists company name",
        )

        result = GetAllRoadsCommandHandler.handle(command=command)

        self.assertEqual(len(result), 0)
