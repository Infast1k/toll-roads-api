from django.contrib import admin

from company.models import Account, Company


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "oid",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "created_at",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "created_at",
    )
    search_fields = ("email",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "oid",
        "name",
        "account__email",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "name",
        "account__email",
    )
