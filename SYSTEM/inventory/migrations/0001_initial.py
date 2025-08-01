# Generated by Django 5.1.3 on 2025-07-02 13:37

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Batch",
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
                (
                    "certification",
                    models.CharField(
                        choices=[("ORG", "Organic"), ("CON", "Conventional")],
                        max_length=3,
                    ),
                ),
                (
                    "lot_number",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Auto-incremented yearly, but editable",
                        null=True,
                    ),
                ),
                (
                    "drier_number",
                    models.CharField(blank=True, default="00", max_length=3),
                ),
                ("batch_number", models.CharField(max_length=50, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "driver_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "vehicle_registration",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("no_of_bags", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "total_quantity_received",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FieldOfficer",
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
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Field Officer Name"),
                ),
                (
                    "field_officer_code",
                    models.CharField(
                        help_text="A unique alphanumeric code for the Field Officer.",
                        max_length=20,
                        unique=True,
                        verbose_name="Field Officer Code",
                    ),
                ),
            ],
            options={
                "verbose_name": "Field Officer",
                "verbose_name_plural": "Field Officers",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Region",
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
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Region Name"
                    ),
                ),
                (
                    "region_code",
                    models.IntegerField(
                        help_text="A unique numerical code for the region (e.g., 1, 10, 100)",
                        unique=True,
                        verbose_name="Region Code",
                    ),
                ),
            ],
            options={
                "verbose_name": "Region",
                "verbose_name_plural": "Regions",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ReceivingFOAverage",
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
                ("date", models.DateField()),
                ("fo_name", models.CharField(max_length=100)),
                ("average_skr", models.DecimalField(decimal_places=2, max_digits=10)),
                ("total_samples", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.batch",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Receiving FO Averages",
            },
        ),
        migrations.CreateModel(
            name="ReceivingNormalSKR",
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
                ("sample_number", models.PositiveIntegerField()),
                (
                    "good_q",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "insect_damaged",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "mold",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "immature",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                (
                    "moisture",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "spillage",
                    models.DecimalField(
                        decimal_places=2, default=Decimal("0.00"), max_digits=6
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.batch",
                    ),
                ),
                (
                    "field_officer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.fieldofficer",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Receiving Normal SKRs",
                "unique_together": {("batch", "field_officer", "sample_number")},
            },
        ),
        migrations.CreateModel(
            name="Sizing",
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
                (
                    "size_0",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        help_text="Quantity for Size 0",
                        max_digits=10,
                    ),
                ),
                (
                    "size_1l",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        help_text="Quantity for Size 1L",
                        max_digits=10,
                    ),
                ),
                (
                    "size_1s",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        help_text="Quantity for Size 1S",
                        max_digits=10,
                    ),
                ),
                (
                    "size_1xs",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        help_text="Quantity for Size 1XS",
                        max_digits=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "normal_skr_entry",
                    models.OneToOneField(
                        help_text="The Normal SKR entry this sizing data belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sizing_data",
                        to="inventory.receivingnormalskr",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Sizing Data",
            },
        ),
        migrations.CreateModel(
            name="Store",
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
                ("name", models.CharField(max_length=100, verbose_name="Store Name")),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.region",
                        verbose_name="Region",
                    ),
                ),
            ],
            options={
                "verbose_name": "Store",
                "verbose_name_plural": "Stores",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="fieldofficer",
            name="store",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="inventory.store",
                verbose_name="Store",
            ),
        ),
        migrations.CreateModel(
            name="ReceivingSKRWithMoisture",
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
                ("sample_number", models.PositiveIntegerField()),
                (
                    "good_q",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "insect_damaged",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "mold",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "immature",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "moisture",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "spillage",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "skr",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "batch",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.batch",
                    ),
                ),
                (
                    "field_officer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.fieldofficer",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Receiving SKRs With Moisture",
                "unique_together": {("batch", "field_officer", "sample_number")},
            },
        ),
        migrations.AddConstraint(
            model_name="store",
            constraint=models.UniqueConstraint(
                fields=("name", "region"), name="unique_store_name_region"
            ),
        ),
    ]
