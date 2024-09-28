from django.urls import path

from road.views.road_views import RoadDetailView, RoadsView


urlpatterns = [
    path('', RoadsView.as_view()),
    path('<uuid:road_oid>/', RoadDetailView.as_view()),
]
