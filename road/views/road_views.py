from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from road.commands.create_road_commands import (
    CreateRoadCommand,
    CreateRoadCommandHandler,
)
from road.serializers.create_road_serializer import (
    InputCreateRoadSerializer,
    OutputCreateRoadSerializer,
)


class RoadsView(APIView):
    permission_classes = (IsAuthenticated,)

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
