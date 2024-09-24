from django.contrib import admin

from road.models import Road


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    list_display = (
        "oid",
        "name",
        "locations",
        "company__name",
        "created_at",
    )
    list_filter = (
        "created_at",
    )
    search_fields = (
        "name",
        "locations",
        "company__name",
        "company__account__email",
    )
