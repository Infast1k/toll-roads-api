from dataclasses import dataclass
from django.db.models.query import QuerySet

from core.base.commands import BaseCommand, BaseCommandHandler
from road.models import Road


@dataclass(frozen=True)
class GetAllRoadsCommand(BaseCommand):
    company_name: str


@dataclass(eq=False, frozen=True)
class GetAllRoadsCommandHandler(
    BaseCommandHandler[GetAllRoadsCommand, QuerySet[Road]],
):
    @staticmethod
    def handle(command: GetAllRoadsCommand) -> QuerySet[Road]:
        roads = Road.objects.filter(company__name=command.company_name)
        return roads
