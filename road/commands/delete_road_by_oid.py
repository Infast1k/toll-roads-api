from dataclasses import dataclass
from uuid import UUID

from rest_framework import exceptions

from core.base.commands import BaseCommand, BaseCommandHandler
from road.models import Road


@dataclass(frozen=True)
class DeleteRoadByOidCommand(BaseCommand):
    road_oid: UUID
    company_name: str


@dataclass(eq=False, frozen=True)
class DeleteRoadByOidCommandHandler(
    BaseCommandHandler[DeleteRoadByOidCommand, None],
):
    @staticmethod
    def handle(command: DeleteRoadByOidCommand) -> None:
        company_roads = Road.objects.filter(company__name=command.company_name)
        road = company_roads.filter(oid=command.road_oid).first()
        if not road:
            raise exceptions.NotFound(
                detail=f"road with {command.road_oid} oid not found",
            )

        road.delete()
