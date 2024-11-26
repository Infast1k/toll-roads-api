from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from company.serializers import (
    InputLoginSerializer,
    InputRefreshSerializer,
    InputRegisterCompanySerializer,
    OutputCompanySerializer,
    OutputLoginSerializer,
)
from company.services import AccountService, CompanyService, JWTService


class RegisterCompanyView(APIView):
    account_service = AccountService
    company_service = CompanyService

    def post(self, request: HttpRequest) -> Response:
        company_serializer = InputRegisterCompanySerializer(data=request.data)
        company_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            account = self.account_service.create_account(
                email=company_serializer.validated_data.get("account").get(
                    "email",
                ),
                password=company_serializer.validated_data.get("account").get(
                    "password",
                ),
            )
            company = self.company_service.create_company(
                company_name=company_serializer.validated_data["name"],
                account=account,
            )

        response_data = OutputCompanySerializer(company).data

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginCompanyView(APIView):
    account_service = AccountService
    jwt_service = JWTService

    def post(self, request: HttpRequest) -> Response:
        login_serializer = InputLoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        account = self.account_service.get_account_by_email(
            email=login_serializer.validated_data.get("email"),
        )
        tokens = self.jwt_service.generate_tokens(account_oid=account.oid)

        response_data = OutputLoginSerializer(tokens).data

        return Response(response_data, status=status.HTTP_200_OK)


class RefreshTokensView(APIView):
    jwt_service = JWTService

    def post(self, request: HttpRequest) -> Response:
        refresh_serializer = InputRefreshSerializer(data=request.data)
        refresh_serializer.is_valid(raise_exception=True)

        tokens = self.jwt_service.refresh_tokens(
            refresh_token=refresh_serializer.validated_data["refresh_token"],
        )

        response_data = OutputLoginSerializer(tokens).data

        return Response(response_data, status=status.HTTP_200_OK)


class Profile(APIView):
    company_service = CompanyService
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest) -> Response:
        company_oid = request.user.company.oid
        company = self.company_service.get_company_by_oid(oid=company_oid)
        response_data = OutputCompanySerializer(company).data
        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest) -> Response:
        company_oid = request.user.company.oid
        self.company_service.delete_company_by_oid(oid=company_oid)

        return Response(status=status.HTTP_204_NO_CONTENT)
