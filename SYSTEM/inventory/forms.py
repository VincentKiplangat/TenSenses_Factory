from django import forms
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from .models import (
    Batch,
    ReceivingNormalSKR,
    ReceivingSKRWithMoisture,
    Region,
    Store,
    FieldOfficer
)


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            'certification',
            'lot_number',
            'drier_number',
            'driver_name',
            'vehicle_registration',
            'no_of_bags',
            'total_quantity_received'
        ]
        widgets = {
            'certification': forms.Select(attrs={'class': 'form-control rounded-md'}),
            'lot_number': forms.NumberInput(attrs={'class': 'form-control rounded-md'}),
            'drier_number': forms.NumberInput(attrs={
                'class': 'form-control rounded-md',
                'min': 1, 'max': 32
            }),
            'driver_name': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'vehicle_registration': forms.TextInput(attrs={'class': 'form-control rounded-md'}),
            'no_of_bags': forms.NumberInput(attrs={'class': 'form-control rounded-md'}),
            'total_quantity_received': forms.NumberInput(attrs={'class': 'form-control rounded-md'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Auto-fill lot number for new batches only
        if not self.instance.pk:
            current_year = now().year
            latest_batch = Batch.objects.filter(
                created_at__year=current_year
            ).order_by('-lot_number').first()

            next_lot = (latest_batch.lot_number or 0) + 1 if latest_batch else 1
            self.fields['lot_number'].initial = next_lot

    def clean(self):
        cleaned_data = super().clean()
        certification = cleaned_data.get('certification')
        lot_number = cleaned_data.get('lot_number')
        drier_number = cleaned_data.get('drier_number')

        check_date = (
            self.instance.created_at.date()
            if self.instance and self.instance.created_at
            else now().date()
        )

        if certification and lot_number is not None and drier_number is not None:
            qs = Batch.objects.filter(
                certification=certification,
                lot_number=lot_number,
                drier_number=drier_number,
                created_at__year=check_date.year
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError(
                    f"A batch with certification '{certification}', lot '{lot_number}', "
                    f"and drier '{drier_number}' already exists for year {check_date.year}."
                )

        return cleaned_data


class ReceivingNormalSKRForm(forms.ModelForm):
    class Meta:
        model = ReceivingNormalSKR
        exclude = ['skr']  # SKR is calculated


class ReceivingSKRWithMoistureForm(forms.ModelForm):
    class Meta:
        model = ReceivingSKRWithMoisture
        exclude = ['skr']


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'region_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., East Africa, North America'}),
            'region_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 101, 205'}),
        }
        labels = {
            'name': 'Region Name',
            'region_code': 'Region Code',
        }
        help_texts = {
            'region_code': 'A unique whole number for the region.',
        }

    # Custom validation for non-negative region_code
    def clean_region_code(self):
        region_code = self.cleaned_data.get('region_code')
        if region_code is not None and region_code <= 0:
            raise forms.ValidationError("Region code must be a positive number.")
        return region_code


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'region']


class FieldOfficerForm(forms.ModelForm):
    class Meta:
        model = FieldOfficer
        fields = ['name', 'field_officer_code', 'store']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field Officer Name'}),
            'field_officer_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., FO001'}),
            'store': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Field Officer Name',
            'field_officer_code': 'Field Officer Code',
            'store': 'Assigned Store',
        }

    def clean_field_officer_code(self):
        code = self.cleaned_data.get('field_officer_code')
        if not code:
            raise forms.ValidationError("Field Officer Code is required.")
        return code
