from django.conf import settings
import jwt
from rest_framework import authentication, exceptions
from rest_framework.request import HttpRequest

from company.models import Account


class CustomAuthBackend(authentication.BaseAuthentication):
    def authenticate(self, request: HttpRequest) -> list:
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return None

        token = auth_header.split(" ")[-1]
        if token == "":
            return None

        try:
            company_oid = jwt.decode(
                jwt=token,
                algorithms=["HS256"],
                key=settings.JWT_SECRET,
            ).get("sub")

            if company_oid == "":
                return None

            account = Account.objects.get(pk=company_oid)
            return (account, None)

        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed("Account not found")
        except Exception:
            return None
