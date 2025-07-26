# inventory/models.py
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class Batch(models.Model):
    CERT_ORG = 'ORG'
    CERT_CON = 'CON'

    CERTIFICATION_CHOICES = [
        (CERT_ORG, 'Organic'),
        (CERT_CON, 'Conventional'),
    ]

    certification = models.CharField(max_length=3, choices=CERTIFICATION_CHOICES)
    lot_number = models.PositiveIntegerField(
        help_text="Auto-incremented yearly, but editable",
        null=True, blank=True
    )
    drier_number = models.CharField(max_length=3, blank=True, default='00')
    batch_number = models.CharField(max_length=50, unique=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    driver_name = models.CharField(max_length=100, null=True, blank=True)
    vehicle_registration = models.CharField(max_length=50, null=True, blank=True)
    no_of_bags = models.PositiveIntegerField(null=True, blank=True)
    total_quantity_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='batches_created'
    )

    def clean(self):
        super().clean()
        if self.lot_number:
            year = self.created_at.year if self.created_at else now().year
            duplicate = Batch.objects.filter(
                lot_number=self.lot_number,
                created_at__year=year
            )
            if self.pk:
                duplicate = duplicate.exclude(pk=self.pk)
            if duplicate.exists():
                raise ValidationError(
                    f"Lot number {self.lot_number} already exists for the year {year}."
                )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new and not self.created_at:
            self.created_at = now()

        current_year = self.created_at.year

        if is_new:
            if not self.lot_number:
                latest_batch = Batch.objects.filter(
                    created_at__year=current_year
                ).order_by('-lot_number').first()

                if latest_batch:
                    self.lot_number = latest_batch.lot_number + 1
                else:
                    self.lot_number = 1  # Reset for new year

        # Generate or regenerate batch_number
        should_regenerate = is_new or any([
            not self.batch_number,
            self.certification != getattr(self, '_original_cert', self.certification),
            self.lot_number != getattr(self, '_original_lot', self.lot_number),
            self.drier_number != getattr(self, '_original_drier', self.drier_number),
        ])

        if should_regenerate:
            day_of_year = self.created_at.timetuple().tm_yday
            lot = str(self.lot_number)
            drier = str(self.drier_number).zfill(3)
            self.batch_number = f"{self.certification}.{day_of_year:03d}.LOT{lot}.{drier}"

        self.clean()
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store original values to detect changes
        self._original_cert = getattr(self, 'certification', None)
        self._original_lot = getattr(self, 'lot_number', None)
        self._original_drier = getattr(self, 'drier_number', None)

    def __str__(self):
        return self.batch_number

    def certification_verbose(self):
        return dict(self.CERTIFICATION_CHOICES).get(self.certification, "Unknown")


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Region Name")
    region_code = models.IntegerField(unique=True, verbose_name="Region Code",
                                      help_text="A unique numerical code for the region (e.g., 1, 10, 100)")

    class Meta:
        ordering = ['name']
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        return f"{self.name} ({self.region_code})"


class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Store Name")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Region")

    class Meta:
        # Add the UniqueConstraint here
        # This ensures that the combination of 'name' and 'region' is unique
        constraints = [
            models.UniqueConstraint(fields=['name', 'region'], name='unique_store_name_region')
        ]
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ['name']  # Consistent ordering for Store objects

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class FieldOfficer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Field Officer Name")
    field_officer_code = models.CharField(  # This is now the CharField
        max_length=20,  # Ensure max_length matches the one set in Phase 1
        unique=True,  # It must be unique and non-nullable
        verbose_name="Field Officer Code",  # Revert to original verbose name
        help_text="A unique alphanumeric code for the Field Officer."  # Revert help text
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Store")

    class Meta:
        ordering = ['name']
        verbose_name = "Field Officer"
        verbose_name_plural = "Field Officers"
        # No unique constraint on name or (name, store)

    def __str__(self):
        # Now __str__ can reliably use the alphanumeric code
        return f"{self.name} ({self.field_officer_code}) - {self.store.name}"


class ReceivingNormalSKR(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    field_officer = models.ForeignKey(FieldOfficer, on_delete=models.CASCADE, null=True, blank=True)
    sample_number = models.PositiveIntegerField()

    good_q = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    insect_damaged = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    mold = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    immature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    moisture = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    spillage = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))  # Use Decimal for default
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('batch', 'field_officer', 'sample_number')
        verbose_name_plural = "Receiving Normal SKRs"

    @property
    def skr(self):
        if self.good_q is not None:
            return round(self.good_q / 5, 2)
        return None

    def __str__(self):
        fo_name = self.field_officer.name if self.field_officer else 'N/A'
        return f"Batch {self.batch.batch_number} - FO {fo_name} - Sample {self.sample_number}"


class ReceivingSKRWithMoisture(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    field_officer = models.ForeignKey(FieldOfficer, on_delete=models.CASCADE, null=True, blank=True)
    sample_number = models.PositiveIntegerField()

    good_q = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    insect_damaged = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    immature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moisture = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spillage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    skr = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        fo_name = self.field_officer.name if self.field_officer else 'N/A'
        return f"Moisture SKR - {self.batch.batch_number} - FO {fo_name} - Sample {self.sample_number}"

    class Meta:
        unique_together = ('batch', 'field_officer', 'sample_number')
        verbose_name_plural = "Receiving SKRs With Moisture"


class ReceivingFOAverage(models.Model):
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    date = models.DateField()
    fo_name = models.CharField(max_length=100)
    average_skr = models.DecimalField(max_digits=10, decimal_places=2)
    total_samples = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.batch.batch_number} - {self.fo_name}"

    class Meta:
        verbose_name_plural = "Receiving FO Averages"


class Sizing(models.Model):
    normal_skr_entry = models.OneToOneField(
        ReceivingNormalSKR,
        on_delete=models.CASCADE,
        related_name='sizing_data',
        help_text="The Normal SKR entry this sizing data belongs to."
    )
    size_0 = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                 help_text="Quantity for Size 0")
    size_1l = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                  help_text="Quantity for Size 1L")
    size_1s = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                  help_text="Quantity for Size 1S")
    size_1xs = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   help_text="Quantity for Size 1XS")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sizing Data"

    def __str__(self):
        return f"Sizing for Sample {self.normal_skr_entry.sample_number} (Batch {self.normal_skr_entry.batch.batch_number})"
