from uuid import uuid4
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

from company.models import Account, Company
from road.models import Road


class UpdateRoadViewTest(APITestCase):
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

        self.road = Road.objects.create(
            name="Test Road",
            locations="Test Locations",
            company=self.first_company,
        )

        self.valid_input_data = [
            {
                "road_oid": self.road.oid,
                "name": "new test road name",
                "locations": "new test locations",
            },
            {
                "road_oid": self.road.oid,
                "locations": "new test locations",
            },
            {
                "road_oid": self.road.oid,
                "name": "new test road name",
            },
            {
                "road_oid": self.road.oid,
            },
        ]

        self.invalid_input_data = [
            {
                "road_oid": uuid4(),
                "token": self.first_access,
                "code": 400,
            },
            {
                "road_oid": self.road.oid,
                "token": self.second_access,
                "code": 400,
            },
        ]

    def test_valid_case(self):
        for data in self.valid_input_data:
            response = self.client.put(
                path=self.roads_url+f"{data.pop('road_oid')}/",
                data=data,
                headers={"Authorization": f"Bearer {self.first_access}"},
            )

            self.assertEqual(response.status_code, 200)

    def test_invalid_case(self):
        for data in self.invalid_input_data:
            response = self.client.put(
                path=self.roads_url+f"{data.pop('road_oid')}/",
                data={},
                headers={"Authorization": f"Bearer {data.get('token')}"},
            )

            self.assertEqual(response.status_code, data.get("code"))

    def test_permission_classes(self):
        result = self.client.put(
            path=self.roads_url+f"{self.road.oid}/",
            data={},
        )

        self.assertEqual(result.status_code, 403)
