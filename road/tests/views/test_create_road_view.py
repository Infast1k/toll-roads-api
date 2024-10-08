from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

from company.models import Account, Company
from road.models import Road


class CreateRoadViewTest(APITestCase):
    def setUp(self):
        self.roads_url = "/api/v1/roads/"
        self.auth_url = "/api/v1/auth/sign-in/"

        self.fist_account = Account.objects.create(
            email="testemail@mail.ru",
            password=make_password("testpassword"),
        )

        self.first_company = Company.objects.create(
            name="Test First Company",
            account=self.fist_account,
        )

        self.first_access = self.client.post(
            path=self.auth_url,
            data={"email": "testemail@mail.ru", "password": "testpassword"},
        ).data.get("access_token")

        self.second_account = Account.objects.create(
            email="testemail2@mail.ru",
            password=make_password("testpassword"),
        )

        self.second_company = Company.objects.create(
            name="Test Second Company",
            account=self.second_account,
        )

        self.second_access = self.client.post(
            path=self.auth_url,
            data={"email": "testemail2@mail.ru", "password": "testpassword"},
        ).data.get("access_token")

        Road.objects.create(
            name="Test Road",
            locations="Test Locations",
            company=self.first_company,
        )

        self.invalid_input_data = [
            {
                "road_name": "Test Road",
                "road_locations": "Test Locations",
                "company_name": self.first_company.name,
            },
            {
                "road_name": "Test Road",
                "company_name": self.first_company.name,
            },
            {
                "road_name": "Test Road",
                "road_locations": "Test Locations",
            },
            {},
        ]

    def test_success_case(self):
        result = self.client.post(
            path=self.roads_url,
            data={
                "road_name": "new road name",
                "road_locations": "new road locations",
                "company_name": self.first_company.name,
            },
            headers={"Authorization": f"Bearer {self.first_access}"},
        )

        self.assertEqual(result.status_code, 201)
        self.assertIsNotNone(result.data)
        self.assertEqual(result.data.get("name"), "new road name")
        self.assertEqual(result.data.get("locations"), "new road locations")

    def test_invalid_case(self):
        for data in self.invalid_input_data:
            result = self.client.post(
                path=self.roads_url,
                data={
                    "road_name": "Test Road",
                    "road_locations": "Test Locations",
                    "company_name": self.first_company.name,
                },
                headers={"Authorization": f"Bearer {self.first_access}"},
            )

            self.assertEqual(result.status_code, 400)

    def test_permission_classes(self):
        result = self.client.get(
            path=self.roads_url,
        )

        self.assertEqual(result.status_code, 403)
