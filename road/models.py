from django.db import models

from core.models import BaseModel


class Road(BaseModel):
    """Model for storing data about roads."""

    name = models.CharField(
        max_length=255,
        unique=True,
    )
    locations = models.CharField(
        max_length=255,
        unique=True,
    )
    company = models.ForeignKey(
        to="company.Company",
        on_delete=models.CASCADE,
        related_name="roads",
        db_index=True,
    )
    # TODO: think about metadata like distance, duration, max speed and etc.

    def __str__(self) -> str:
        return f"{self.name} - {self.company.name}"

    class Meta:
        verbose_name = "Road"
        verbose_name_plural = "Roads"
        db_table = "roads"
        ordering = ["-created_at"]
