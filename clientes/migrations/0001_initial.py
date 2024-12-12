# Generated by Django 4.2.17 on 2024-12-11 01:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                (
                    "cpf",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="CPF deve conter exatamente 11 dígitos numéricos",
                                regex="^\\d{11}$",
                            )
                        ],
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["nome"],
            },
        ),
    ]
