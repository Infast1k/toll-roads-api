# Generated by Django 5.1.1 on 2024-09-24 06:48

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("company", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Road",
            fields=[
                (
                    "oid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("locations", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="roads",
                        to="company.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Road",
                "verbose_name_plural": "Roads",
                "db_table": "roads",
                "ordering": ["-created_at"],
            },
        ),
    ]
