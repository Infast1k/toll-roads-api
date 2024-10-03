from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.db import transaction

from company.models import Account, Company
from core.base.commands import BaseCommand, BaseCommandHandler


@dataclass(frozen=True)
class LoginCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class AuthTokens:
    access_token: str
    refresh_token: str


@dataclass(eq=False, frozen=True)
class LoginCommandHandler(BaseCommandHandler[LoginCommand, AuthTokens]):

    @staticmethod
    def handle(command: LoginCommand) -> AuthTokens:
        account = Account.objects.get(email=command.email)

        access_token = jwt.encode(
            payload={
                "sub": str(account.oid),
                "exp": datetime.now() + timedelta(
                    minutes=settings.JWT_EXP_IN_MINUTES,
                ),
            },
            key=settings.JWT_SECRET,
            algorithm="HS256",
        )

        refresh_token = uuid4()

        cache.set(
            key=str(refresh_token),
            value=str(account.oid),
            timeout=settings.REFRESH_EXP_IN_DAYS,
        )

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )


@dataclass(frozen=True)
class RegisterCompanyCommand(BaseCommand):
    name: str
    email: str
    password: str


@dataclass(eq=False, frozen=True)
class RegisterCompanyCommandHandler(
    BaseCommandHandler[RegisterCompanyCommand, Company],
):
    @staticmethod
    @transaction.atomic
    def handle(command: RegisterCompanyCommand) -> Company:
        account: Account = Account.objects.create(
            email=command.email,
            password=make_password(command.password),
        )
        company: Company = Company.objects.create(
            name=command.name,
            account=account,
        )

        # TODO: send email message for account activation

        return company
