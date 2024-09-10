from django.test import TestCase
from django.utils.timezone import localtime

from company.models import Account, Company
from company.serializers.register_serializers import (
    InputRegisterCompanySerializer,
    OutputRegisterCompanySerializer,
)


class RegisterCompanySerializersTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Company 1",
            "account": {
                "email": "ZTqZ5@example.com",
                "password": "password",
            },
        }

        self.invalid_data = [
            {
                "name": "Company 2",
                "account": {
                    "email": "ZTqZ5@example.com",
                },
            },
            {
                "name": "Company 3",
                "account": {
                    "password": "password",
                },
            },
            {
                "name": "Company 4",
                "account": {},
            },
            {
                "name": "Company 5",
                "account": "account",
            },
            {
                "name": "Company 6",
                "account": {
                    "email": "ZTqZ5@example.com",
                    "password": "pasword",
                },
            },
            {
                "account": {
                    "email": "ZTqZ5@example.com",
                    "password": "pasword",
                }
            },
            {
                "name": True,
                "account": {
                    "email": "ZTqZ5@example.com",
                    "password": "password",
                },
            },
        ]

    def test_valid_data(self):
        input_serializer = InputRegisterCompanySerializer(data=self.valid_data)

        self.assertTrue(input_serializer.is_valid())
        self.assertEqual(input_serializer.validated_data, self.valid_data)

        account = Account.objects.create(
            email=input_serializer.validated_data["account"]["email"],
            password=input_serializer.validated_data["account"]["password"],
        )

        company = Company.objects.create(
            name=input_serializer.validated_data["name"],
            account=account,
        )

        output_serializer = OutputRegisterCompanySerializer(company).data

        valid_output_test_data = {
            "oid": str(company.oid),
            "name": company.name,
            "account": {
                "oid": str(account.oid),
                "email": account.email,
                "is_active": account.is_active,
                "is_staff": account.is_staff,
                "is_superuser": account.is_superuser,
                "created_at": localtime(company.created_at).strftime(
                    r"%d.%m.%Y %H:%M:%S"
                ),
            },
            "created_at": localtime(company.created_at).strftime(
                r"%d.%m.%Y %H:%M:%S"
            ),
        }

        self.assertEqual(output_serializer, valid_output_test_data)

    def test_invalid_data(self):
        for data in self.invalid_data:
            input_serializer = InputRegisterCompanySerializer(data=data)
            self.assertFalse(input_serializer.is_valid())
