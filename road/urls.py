from django.urls import path

from road.views import RoadsView, RoadDetailView


urlpatterns = [
    path('', RoadsView.as_view()),
    path('<uuid:road_oid>/', RoadDetailView.as_view()),
]
