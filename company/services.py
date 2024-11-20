from datetime import datetime, timedelta
from uuid import UUID, uuid4

import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.cache import cache

from company.models import Account, Company


class AccountService:
    @classmethod
    def get_account_by_email(cls, email) -> Account:
        account = Account.objects.get(email=email)

        return account

    @classmethod
    def create_account(cls, email: str, password: str) -> Account:
        account = Account.objects.create(
            email=email,
            password=make_password(password),
        )

        return account


class CompanyService:
    @classmethod
    def create_company(cls, company_name: str, account: Account) -> Company:
        company = Company.objects.create(
            name=company_name,
            account=account,
        )

        return company


class JWTService:
    @classmethod
    def generate_tokens(cls, account_oid: UUID) -> dict[str, str | UUID]:
        access_token = jwt.encode(
            payload={
                "sub": str(account_oid),
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
            value=str(account_oid),
            timeout=settings.REFRESH_EXP_IN_DAYS,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @classmethod
    def refresh_tokens(cls, refresh_token: str) -> dict[str, str | UUID]:
        account_oid = cache.get(key=refresh_token)

        if account_oid is None:
            raise ValueError("Invalid refresh token")

        cache.delete(key=refresh_token)

        tokens = cls.generate_tokens(account_oid=account_oid)

        return tokens
