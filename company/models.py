from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from company.managers import AccountManager
from core.models import BaseModel


class Account(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Model for storing credentials for companies."""

    email = models.EmailField(
        unique=True,
        db_index=True,
    )
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

    objects = AccountManager()
    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        db_table = "accounts"
        ordering = ["-created_at"]


class Company(BaseModel):
    """Model for storing data about companies without credentials."""

    name = models.CharField(
        max_length=75,
        unique=True,
        db_index=True,
    )
    tokens = models.PositiveSmallIntegerField(default=3)
    account = models.OneToOneField(
        to=Account,
        on_delete=models.CASCADE,
        related_name="company",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "companies"
        ordering = ["-created_at"]
