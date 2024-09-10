from django.urls import path

from company.views.auth_views import RegisterCompanyView


urlpatterns = [
    path("sign-up/", RegisterCompanyView.as_view()),
]
