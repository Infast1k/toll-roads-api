from rest_framework import serializers

from company.models import Account, Company


class InputLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        account = Account.objects.filter(email=data["email"]).first()

        if not account:
            raise serializers.ValidationError("invalid credentials")
        if not account.check_password(data["password"]):
            raise serializers.ValidationError("invalid credentials")

        return data


class OutputLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


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


class OutputAccountSerializer(serializers.ModelSerializer):
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


class OutputCompanySerializer(serializers.ModelSerializer):
    account = OutputAccountSerializer(many=False)

    class Meta:
        model = Company
        fields = (
            "oid",
            "name",
            "account",
            "created_at",
        )


class InputRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.UUIDField()
