from dataclasses import dataclass
from uuid import UUID

from core.base.commands import BaseCommand, BaseCommandHandler
from road.models import Road


@dataclass(frozen=True)
class GetRoadByOidCommand(BaseCommand):
    road_oid: UUID


@dataclass(eq=False, frozen=True)
class GetRoadByOidCommandHandler(
    BaseCommandHandler[GetRoadByOidCommand, Road],
):
    @staticmethod
    def handle(command: GetRoadByOidCommand) -> Road:
        return Road.objects.get(oid=command.road_oid)
