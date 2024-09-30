from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core.base.commands import BaseCommand, BaseCommandHandler
from road.models import Road


@dataclass(frozen=True)
class UpdateRoadCommand(BaseCommand):
    oid: UUID
    name: Optional[str]
    locations: Optional[str]


@dataclass(eq=False, frozen=True)
class UpdateRoadCommandHandler(BaseCommandHandler[UpdateRoadCommand, Road]):
    @staticmethod
    def handle(command: UpdateRoadCommand) -> Road:
        road = Road.objects.get(oid=command.oid)

        if command.name is not None:
            road.name = command.name
        if command.locations is not None:
            road.locations = command.locations
        road.save()

        return road
