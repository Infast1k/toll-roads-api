from django.urls import path

from company.views import LoginCompanyView, RegisterCompanyView


urlpatterns = [
    path("sign-up/", RegisterCompanyView.as_view()),
    path("sign-in/", LoginCompanyView.as_view()),
]
