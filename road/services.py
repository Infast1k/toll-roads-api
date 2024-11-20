from uuid import UUID

from django.db.models.query import QuerySet

from company.models import Company
from road.models import Road


class RoadService:
    @classmethod
    def get_roads_by_company_name(cls, company_name: str) -> QuerySet[Road]:
        roads = Road.objects.filter(company__name=company_name)
        return roads

    @classmethod
    def create_road(
        cls, road_name: str, road_locations: str, company_name: str
    ) -> Road:
        company = Company.objects.get(name=company_name)

        road = Road.objects.create(
            name=road_name,
            locations=road_locations,
            company=company,
        )

        return road

    @classmethod
    def update_road(
        cls,
        road_oid: UUID,
        road_name: str | None,
        road_locations: str | None,
        company_name: str,
    ) -> Road:
        company_roads = Road.objects.filter(company__name=company_name)
        road = company_roads.get(oid=road_oid)

        if road_name is not None:
            road.name = road_name
        if road_locations is not None:
            road.locations = road_locations
        road.save()

        return road

    @classmethod
    def delete_road_by_oid(cls, road_oid: UUID, company_name: str) -> None:
        company_roads = Road.objects.filter(company__name=company_name)
        road = company_roads.get(oid=road_oid)

        road.delete()
