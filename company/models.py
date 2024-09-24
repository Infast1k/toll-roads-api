from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from company.managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    """Model for storing credentials for companies."""

    oid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        db_index=True,
        editable=False,
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
    )
    # TODO: change is_active to false after adding email verification
    is_active = models.BooleanField(
        blank=True,
        default=True,
    )
    is_staff = models.BooleanField(
        blank=True,
        default=False,
    )
    is_superuser = models.BooleanField(
        blank=True,
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    objects = AccountManager()
    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        db_table = "accounts"
        ordering = ["-created_at"]


class Company(models.Model):
    """Model for storing data about companies without credentials."""

    oid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        db_index=True,
        editable=False,
    )
    name = models.CharField(
        max_length=75,
        unique=True,
        db_index=True,
    )
    account = models.OneToOneField(
        to=Account,
        on_delete=models.CASCADE,
        related_name="company",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "companies"
        ordering = ["-created_at"]
