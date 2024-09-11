from rest_framework import serializers

from company.models import Account


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
