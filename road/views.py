from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from road.commands import (
    CreateRoadCommand,
    CreateRoadCommandHandler,
    DeleteRoadByOidCommand,
    DeleteRoadByOidCommandHandler,
    GetAllRoadsCommand,
    GetAllRoadsCommandHandler,
    UpdateRoadCommand,
    UpdateRoadCommandHandler,
)
from road.serializers import (
    InputCreateRoadSerializer,
    InputDeleteRoadSerializer,
    InputUpdateRoadSerializer,
    OutputRoadSerializer,
)


class RoadsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest) -> Response:
        company_name = request.user.company.name

        command = GetAllRoadsCommand(company_name=company_name)
        roads = GetAllRoadsCommandHandler.handle(command=command)

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

        command = CreateRoadCommand(
            road_name=input_serializer.validated_data["road_name"],
            road_locations=input_serializer.validated_data["road_locations"],
            company_name=company_name,
        )
        road = CreateRoadCommandHandler.handle(command=command)

        response_data = OutputRoadSerializer(road).data

        return Response(response_data, status=status.HTTP_201_CREATED)


class RoadDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request: HttpRequest, road_oid: UUID) -> Response:
        company_name = request.user.company.name

        input_serializer = InputUpdateRoadSerializer(data={
            "road_oid": road_oid,
            "name": request.data.get("name", None),
            "locations": request.data.get("locations", None),
            "company_name": company_name,
        })
        input_serializer.is_valid(raise_exception=True)

        command = UpdateRoadCommand(
            road_oid=input_serializer.validated_data["road_oid"],
            name=input_serializer.validated_data["name"],
            locations=input_serializer.validated_data["locations"],
            company_name=company_name,
        )
        road = UpdateRoadCommandHandler.handle(command=command)

        response_data = OutputRoadSerializer(road).data

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, road_oid: UUID) -> Response:
        company_name = request.user.company.name

        input_serializer = InputDeleteRoadSerializer(data={
            "road_oid": road_oid,
            "company_name": company_name,
        })
        input_serializer.is_valid(raise_exception=True)

        command = DeleteRoadByOidCommand(
            road_oid=road_oid,
            company_name=company_name,
        )
        DeleteRoadByOidCommandHandler.handle(command=command)

        return Response(status=status.HTTP_204_NO_CONTENT)
