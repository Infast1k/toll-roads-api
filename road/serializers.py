from rest_framework import serializers

from company.models import Company
from road.models import Road


class InputCreateRoadSerializer(serializers.Serializer):
    road_name = serializers.CharField()
    road_locations = serializers.CharField()
    company_name = serializers.CharField()

    def validate(self, data):
        if not Company.objects.filter(name=data["company_name"]).exists():
            raise serializers.ValidationError(
                "Company with given name not found"
            )

        if Road.objects.filter(name=data["road_name"]).first():
            raise serializers.ValidationError(
                "Road with same name already exists"
            )

        if Road.objects.filter(locations=data["road_locations"]).first():
            raise serializers.ValidationError(
                "Road with same locations already exists"
            )

        return data


class OutputCreateRoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = (
            "oid",
            "name",
            "locations",
            "created_at",
        )


class OutputRoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = (
            "oid",
            "name",
            "locations",
            "created_at",
        )


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


class InputDeleteRoadSerializer(serializers.Serializer):
    road_oid = serializers.UUIDField()

    def validate(self, attrs):
        if not Road.objects.filter(oid=attrs["road_oid"]).exists():
            raise serializers.ValidationError(
                "Road with given oid not found"
            )

        return attrs
