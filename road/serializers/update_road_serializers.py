from rest_framework import serializers

from road.models import Road


class InputUpdateRoadSerializer(serializers.Serializer):
    oid = serializers.UUIDField()
    name = serializers.CharField(allow_null=True)
    locations = serializers.CharField(allow_null=True)

    def validate(self, attrs):
        if not Road.objects.filter(oid=attrs["oid"]).exists():
            raise serializers.ValidationError(
                "Road with given oid not found"
            )

        return attrs
