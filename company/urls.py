from django.urls import path

from company.views import (
    LoginCompanyView,
    Profile,
    RefreshTokensView,
    RegisterCompanyView,
)


urlpatterns = [
    path("auth/sign-up/", RegisterCompanyView.as_view()),
    path("auth/sign-in/", LoginCompanyView.as_view()),
    path("auth/refresh/", RefreshTokensView.as_view()),
	path("profile/", Profile.as_view()),
]
