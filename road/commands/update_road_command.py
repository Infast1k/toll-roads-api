from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from rest_framework import exceptions

from core.base.commands import BaseCommand, BaseCommandHandler
from road.models import Road


@dataclass(frozen=True)
class UpdateRoadCommand(BaseCommand):
    oid: UUID
    name: Optional[str]
    locations: Optional[str]
    company_name: str


@dataclass(eq=False, frozen=True)
class UpdateRoadCommandHandler(BaseCommandHandler[UpdateRoadCommand, Road]):
    @staticmethod
    def handle(command: UpdateRoadCommand) -> Road:
        company_roads = Road.objects.filter(company__name=command.company_name)
        road = company_roads.filter(oid=command.oid).first()

        if not road:
            raise exceptions.NotFound(
                detail=f"road with {command.oid} oid not found",
            )

        if command.name is not None:
            road.name = command.name
        if command.locations is not None:
            road.locations = command.locations
        road.save()

        return road
