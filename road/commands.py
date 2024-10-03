from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from django.db.models.query import QuerySet

from company.models import Company
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


@dataclass(frozen=True)
class CreateRoadCommand(BaseCommand):
    road_name: str
    road_locations: str
    company_name: str


@dataclass(eq=False, frozen=True)
class CreateRoadCommandHandler(BaseCommandHandler[CreateRoadCommand, Road]):
    @staticmethod
    def handle(command: CreateRoadCommand) -> Road:
        company = Company.objects.get(name=command.company_name)

        road = Road.objects.create(
            name=command.road_name,
            locations=command.road_locations,
            company=company,
        )

        return road


@dataclass(frozen=True)
class UpdateRoadCommand(BaseCommand):
    road_oid: UUID
    name: Optional[str]
    locations: Optional[str]
    company_name: str


@dataclass(eq=False, frozen=True)
class UpdateRoadCommandHandler(BaseCommandHandler[UpdateRoadCommand, Road]):
    @staticmethod
    def handle(command: UpdateRoadCommand) -> Road:
        company_roads = Road.objects.filter(company__name=command.company_name)
        road = company_roads.get(oid=command.road_oid)

        if command.name is not None:
            road.name = command.name
        if command.locations is not None:
            road.locations = command.locations
        road.save()

        return road


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
        road = company_roads.get(oid=command.road_oid)

        road.delete()
