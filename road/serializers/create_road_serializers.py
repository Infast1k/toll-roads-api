from rest_framework import serializers

from company.models import Account, Company
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


class OutputCreateRoadSerializer(serializers.ModelSerializer):
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
