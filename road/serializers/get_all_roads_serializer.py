from rest_framework import serializers

from company.models import Company
from road.models import Road


class CompanySerialier(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class OutputGetAllRoadsSerializer(serializers.ModelSerializer):
    company = CompanySerialier(many=False)

    class Meta:
        model = Road
        fields = (
            "oid",
            "name",
            "locations",
            "company",
            "created_at",
        )
