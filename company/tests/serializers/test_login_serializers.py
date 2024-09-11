from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.test import TestCase

from company.models import Account
from company.serializers.login_serializers import (
    InputLoginSerializer,
    OutputLoginSerializer,
)


class LoginSerializerSTest(TestCase):
    def setUp(self):
        Account.objects.create(
            email="test@test.com",
            password=make_password("password"),
        )

        self.valid_input_data = {
            "email": "test@test.com",
            "password": "password",
        }

        self.invalid_input_data = [
            {
                "email": "test@test.com",
                "password": "wrongpassword",
            },
            {
                "email": "wrong_email@test.com",
                "password": "password",
            },
            {
                "password": "password",
            },
            {
                "email": "wrong_email@test.com",
            },
            {
                "email": True,
                "password": "password",
            },
            {
                "email": "test@test.com",
                "password": True,
            },
            {},
        ]

        self.valid_output_data = {
            "access_token": str(uuid4()),
            "refresh_token": str(uuid4()),
        }

        self.invalid_output_data = [
            {
                "access_token": "access_token",
                "refresh_token": True,
            },
            {
                "access_token": True,
                "refresh_token": "refresh_token",
            },
            {
                "access_token": True,
                "refresh_token": True,
            },
            {
                "access_token": "access_token",
            },
            {
                "refresh_token": "refresh_token",
            },
            {},
        ]

    def test_success_login_input_serializer(self):
        serializer = InputLoginSerializer(data=self.valid_input_data)
        self.assertTrue(serializer.is_valid())

    def test_fail_login_input_serializer(self):
        wrong_serializers = []

        for data in self.invalid_input_data:
            wrong_serializers.append(InputLoginSerializer(data=data))

        for serializer in wrong_serializers:
            self.assertFalse(serializer.is_valid())

    def test_success_login_output_serializer(self):
        serializer = OutputLoginSerializer(data=self.valid_output_data)
        self.assertTrue(serializer.is_valid())

    def test_fail_login_output_serializer(self):
        wrong_serializers = []

        for data in self.invalid_output_data:
            wrong_serializers.append(OutputLoginSerializer(data=data))

        for serializer in wrong_serializers:
            self.assertFalse(serializer.is_valid())
