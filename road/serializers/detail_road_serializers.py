from rest_framework import serializers

from company.models import Account, Company
from road.models import Road


class InputGetRoadByOidSerializer(serializers.Serializer):
    road_oid = serializers.UUIDField()

    def validate(self, attrs):

        road_oid = attrs.get("road_oid")
        if not Road.objects.filter(oid=road_oid).exists():
            raise serializers.ValidationError(
                "Road with given oid not found"
            )

        return attrs


class _OutputAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "oid",
            "email",
        )


class _OutputCompanySerializer(serializers.ModelSerializer):
    account = _OutputAccountSerializer(many=False)

    class Meta:
        model = Company
        fields = (
            "oid",
            "name",
            "account",
            "created_at",
        )


class OutupRoadSerializer(serializers.ModelSerializer):
    company = _OutputCompanySerializer(many=False)

    class Meta:
        model = Road
        fields = (
            "oid",
            "name",
            "locations",
            "company",
            "created_at",
        )
