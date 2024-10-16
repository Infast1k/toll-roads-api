from django.db import transaction
from rest_framework import status
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
from company.services import (
    AccountService,
    BaseAccountService,
    BaseCompanyService,
    BaseJWTService,
    CompanyService,
    JWTService,
)


class RegisterCompanyView(APIView):
    account_service: BaseAccountService = AccountService
    company_service: BaseCompanyService = CompanyService

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
    account_service: BaseAccountService = AccountService
    jwt_service: BaseJWTService = JWTService

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
    jwt_service: BaseJWTService = JWTService

    def post(self, request: HttpRequest) -> Response:
        refresh_serializer = InputRefreshSerializer(data=request.data)
        refresh_serializer.is_valid(raise_exception=True)

        tokens = self.jwt_service.refresh_tokens(
            refresh_token=refresh_serializer.validated_data["refresh_token"],
        )

        response_data = OutputLoginSerializer(tokens).data

        return Response(response_data, status=status.HTTP_200_OK)
