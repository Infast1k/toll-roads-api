from dataclasses import dataclass
from uuid import UUID

from core.base.commands import BaseCommand, BaseCommandHandler
from road.models import Road


@dataclass(frozen=True)
class DeleteRoadByOidCommand(BaseCommand):
    road_oid: UUID


@dataclass(eq=False, frozen=True)
class DeleteRoadByOidCommandHandler(
    BaseCommandHandler[DeleteRoadByOidCommand, None],
):
    @staticmethod
    def handle(command: DeleteRoadByOidCommand) -> None:
        road = Road.objects.get(oid=command.road_oid)
        road.delete()
