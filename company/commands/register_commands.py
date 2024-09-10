from dataclasses import dataclass

from django.contrib.auth.hashers import make_password
from django.db import transaction

from company.models import Account, Company
from core.base.commands import BaseCommand, BaseCommandHandler


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
