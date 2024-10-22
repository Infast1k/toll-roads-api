from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

from company.models import Account, Company
from road.models import Road


class GetRoadsView(APITestCase):
    def setUp(self):
        self.roads_url_without_pagination = "/api/v1/roads/"
        self.roads_url_with_pagination = "/api/v1/roads/?limit=5&offset=4"
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

    def test_get_own_roads(self):
        result = self.client.get(
            path=self.roads_url_without_pagination,
            headers={"Authorization": f"Bearer {self.first_access}"},
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data.get("roads")), 1)

    def test_get_other_company_roads(self):
        result = self.client.get(
            path=self.roads_url_without_pagination,
            headers={"Authorization": f"Bearer {self.second_access}"},
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data.get("roads")), 0)

    def test_get_all_roads_with_pagination(self):
        result = self.client.get(
            path=self.roads_url_with_pagination,
            headers={"Authorization": f"Bearer {self.first_access}"},
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data.get("roads")), 0)
        self.assertEqual(result.data.get("total"), 1)

    def test_permission_classes(self):
        result = self.client.get(
            path=self.roads_url_without_pagination,
        )

        self.assertEqual(result.status_code, 403)
