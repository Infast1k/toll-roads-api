from uuid import UUID
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from road.commands import (
    CreateRoadCommand,
    CreateRoadCommandHandler,
    GetAllRoadsCommand,
    GetAllRoadsCommandHandler,
    GetRoadByOidCommand,
    GetRoadByOidCommandHandler,
    UpdateRoadCommand,
    UpdateRoadCommandHandler,
    DeleteRoadByOidCommand,
    DeleteRoadByOidCommandHandler,
)
from road.serializers import (
    InputCreateRoadSerializer,
    InputGetRoadByOidSerializer,
    InputUpdateRoadSerializer,
    OutputCreateRoadSerializer,
    OutputGetAllRoadsSerializer,
    OutupRoadSerializer,
)


class RoadsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest) -> Response:
        company_name = request.user.company.name

        command = GetAllRoadsCommand(company_name=company_name)
        roads = GetAllRoadsCommandHandler.handle(command=command)

        response_data = OutputGetAllRoadsSerializer(roads, many=True).data

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        input_serializer = InputCreateRoadSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        command = CreateRoadCommand(
            road_name=input_serializer.validated_data["road_name"],
            road_locations=input_serializer.validated_data["road_locations"],
            company_name=input_serializer.validated_data["company_name"],
        )
        road = CreateRoadCommandHandler.handle(command=command)

        response_data = OutputCreateRoadSerializer(road).data

        return Response(response_data, status=status.HTTP_201_CREATED)


class RoadDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest, road_oid: UUID) -> Response:
        input_serializer = InputGetRoadByOidSerializer(data={
            "road_oid": road_oid,
        })
        input_serializer.is_valid(raise_exception=True)

        command = GetRoadByOidCommand(road_oid=road_oid)
        road = GetRoadByOidCommandHandler.handle(command=command)

        response_data = OutupRoadSerializer(road).data

        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request: HttpRequest, road_oid: UUID) -> Response:
        input_serializer = InputUpdateRoadSerializer(data={
            "oid": road_oid,
            "name": request.data.get("name", None),
            "locations": request.data.get("locations", None),
        })
        input_serializer.is_valid(raise_exception=True)

        command = UpdateRoadCommand(
            oid=input_serializer.validated_data["oid"],
            name=input_serializer.validated_data["name"],
            locations=input_serializer.validated_data["locations"],
        )
        road = UpdateRoadCommandHandler.handle(command=command)

        response_data = OutupRoadSerializer(road).data

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, road_oid: UUID) -> Response:
        input_serializer = InputGetRoadByOidSerializer(data={
            "road_oid": road_oid,
        })
        input_serializer.is_valid(raise_exception=True)

        command = DeleteRoadByOidCommand(road_oid=road_oid)
        DeleteRoadByOidCommandHandler.handle(command=command)

        return Response(status=status.HTTP_204_NO_CONTENT)
