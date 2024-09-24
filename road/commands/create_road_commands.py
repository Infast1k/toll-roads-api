from dataclasses import dataclass

from company.models import Company
from core.base.commands import BaseCommand, BaseCommandHandler
from road.models import Road


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
