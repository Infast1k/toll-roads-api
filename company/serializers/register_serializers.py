from rest_framework import serializers

from company.models import Account, Company


class _InputRegisterAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8)

    class Meta:
        model = Account
        fields = (
            "email",
            "password",
        )


class InputRegisterCompanySerializer(serializers.ModelSerializer):
    account = _InputRegisterAccountSerializer(many=False)

    class Meta:
        model = Company
        fields = (
            "name",
            "account",
        )


class _OutputRegisterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "oid",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
        )


class OutputRegisterCompanySerializer(serializers.ModelSerializer):
    account = _OutputRegisterAccountSerializer(many=False)

    class Meta:
        model = Company
        fields = (
            "oid",
            "name",
            "account",
            "created_at",
        )
