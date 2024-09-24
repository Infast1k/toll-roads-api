from django.urls import path

from road.views.road_views import RoadsView


urlpatterns = [
    path('', RoadsView.as_view()),
]
