from road.serializers.create_road_serializers import (
    InputCreateRoadSerializer,
    OutputCreateRoadSerializer,
)
from road.serializers.get_all_roads_serializer import (
    OutputGetAllRoadsSerializer,
)
from road.serializers.detail_road_serializers import (
    InputGetRoadByOidSerializer,
    OutupRoadSerializer,
)


__all__ = (
    "InputCreateRoadSerializer",
    "InputGetRoadByOidSerializer",
    "OutputCreateRoadSerializer",
    "OutputGetAllRoadsSerializer",
    "OutupRoadSerializer",
)
