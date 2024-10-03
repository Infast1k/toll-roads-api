from django.urls import path

from company.views import (
    LoginCompanyView,
    RefreshTokensView,
    RegisterCompanyView,
)


urlpatterns = [
    path("sign-up/", RegisterCompanyView.as_view()),
    path("sign-in/", LoginCompanyView.as_view()),
    path("refresh/", RefreshTokensView.as_view()),
]
