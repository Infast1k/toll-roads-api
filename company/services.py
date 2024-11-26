from datetime import datetime, timedelta
from typing import Optional
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

    @classmethod
    def update_account(cls, account_oid: UUID, email: Optional[str]) -> Account:
        account = Account.objects.get(oid=account_oid)

        if email is not None:
            account.email = email
        account.save()

        return account


class CompanyService:
    @classmethod
    def get_company_by_oid(cls, oid: UUID) -> Company:
        company = Company.objects.get(oid=oid)

        return company

    @classmethod
    def create_company(cls, company_name: str, account: Account) -> Company:
        company = Company.objects.create(
            name=company_name,
            account=account,
        )

        return company

    @classmethod
    def update_company(cls, company_oid: UUID, company_name: Optional[str]) -> Company:
        company = cls.get_company_by_oid(oid=company_oid)

        if company_name is not None:
            company.name = company_name
        company.save()

        return company

    @classmethod
    def delete_company_by_oid(cls, oid: UUID) -> None:
        company = cls.get_company_by_oid(oid=oid)
        company.account.delete()


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
