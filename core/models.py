from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    """Model which contains common fields"""

    oid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        db_index=True,
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True
