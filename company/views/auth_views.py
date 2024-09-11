from rest_framework import status
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from company.commands.login_commands import LoginCommand, LoginCommandHandler
from company.commands.register_commands import (
    RegisterCompanyCommand,
    RegisterCompanyCommandHandler,
)
from company.serializers.login_serializers import (
    InputLoginSerializer,
    OutputLoginSerializer,
)
from company.serializers.register_serializers import (
    InputRegisterCompanySerializer,
    OutputRegisterCompanySerializer,
)


class RegisterCompanyView(APIView):
    def post(self, request: HttpRequest) -> Response:
        company_serializer = InputRegisterCompanySerializer(data=request.data)
        company_serializer.is_valid(raise_exception=True)

        command = RegisterCompanyCommand(
            name=company_serializer.validated_data["name"],
            email=company_serializer.validated_data["account"]["email"],
            password=company_serializer.validated_data["account"]["password"],
        )
        company = RegisterCompanyCommandHandler.handle(command=command)

        response_data = OutputRegisterCompanySerializer(company).data

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginCompanyView(APIView):
    def post(self, request: HttpRequest) -> Response:
        login_serializer = InputLoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        command = LoginCommand(
            email=login_serializer.validated_data["email"],
            password=login_serializer.validated_data["password"],
        )
        tokens = LoginCommandHandler.handle(command=command)

        response_data = OutputLoginSerializer(tokens).data

        return Response(response_data, status=status.HTTP_200_OK)
