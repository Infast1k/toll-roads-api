from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from road.serializers import (
    InputCreateRoadSerializer,
    InputDeleteRoadSerializer,
    InputUpdateRoadSerializer,
    OutputRoadSerializer,
)
from road.services import BaseRoadService, RoadService


class RoadsView(APIView):
    permission_classes = (IsAuthenticated,)
    road_service: BaseRoadService = RoadService

    def get(self, request: HttpRequest) -> Response:
        company_name = request.user.company.name

        roads = self.road_service.get_roads_by_company_name(
            company_name=company_name,
        )

        response_data = OutputRoadSerializer(roads, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        company_name = request.user.company.name

        input_serializer = InputCreateRoadSerializer(data={
            "road_name": request.data.get("road_name", None),
            "road_locations": request.data.get("road_locations", None),
            "company_name": company_name,
        })
        input_serializer.is_valid(raise_exception=True)

        road = self.road_service.create_road(
            road_name=input_serializer.validated_data["road_name"],
            road_locations=input_serializer.validated_data["road_locations"],
            company_name=company_name,
        )

        response_data = OutputRoadSerializer(road).data

        return Response(response_data, status=status.HTTP_201_CREATED)


class RoadDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    road_service: BaseRoadService = RoadService

    def put(self, request: HttpRequest, road_oid: UUID) -> Response:
        company_name = request.user.company.name

        input_serializer = InputUpdateRoadSerializer(data={
            "road_oid": road_oid,
            "name": request.data.get("name", None),
            "locations": request.data.get("locations", None),
            "company_name": company_name,
        })
        input_serializer.is_valid(raise_exception=True)

        road = self.road_service.update_road(
            road_oid=input_serializer.validated_data["road_oid"],
            road_name=input_serializer.validated_data["name"],
            road_locations=input_serializer.validated_data["locations"],
            company_name=company_name,
        )

        response_data = OutputRoadSerializer(road).data

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, road_oid: UUID) -> Response:
        company_name = request.user.company.name

        input_serializer = InputDeleteRoadSerializer(data={
            "road_oid": road_oid,
            "company_name": company_name,
        })
        input_serializer.is_valid(raise_exception=True)

        self.road_service.delete_road_by_oid(
            road_oid=road_oid,
            company_name=company_name,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
