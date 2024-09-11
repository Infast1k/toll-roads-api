from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.conf import settings
from django.core.cache import cache

from company.models import Account
from core.base.commands import BaseCommand, BaseCommandHandler


@dataclass(frozen=True)
class LoginCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class AuthTokensCommand:
    access_token: str
    refresh_token: str


@dataclass(eq=False, frozen=True)
class LoginCommandHandler(BaseCommandHandler[LoginCommand, AuthTokensCommand]):

    @staticmethod
    def handle(command: LoginCommand) -> AuthTokensCommand:
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

        return AuthTokensCommand(
            access_token=access_token,
            refresh_token=refresh_token,
        )
