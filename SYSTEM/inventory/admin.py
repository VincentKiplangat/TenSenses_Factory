# inventory/admin.py
from django.contrib import admin
from .models import (
    Batch,
    Region,
    Store,
    FieldOfficer,
    ReceivingNormalSKR,
    ReceivingSKRWithMoisture,
    ReceivingFOAverage,
    Sizing,  # <--- Make sure Sizing is imported here
)

# Define the inline for Sizing data
class SizingInline(admin.StackedInline):
    model = Sizing
    can_delete = False  # Set to True if you want a delete checkbox
    verbose_name_plural = 'Sizing Data'

# Define the custom admin class for ReceivingNormalSKR
class ReceivingNormalSKRAdmin(admin.ModelAdmin):
    inlines = [SizingInline]  # Link the Sizing inline here
    list_display = ('batch', 'field_officer', 'sample_number', 'good_q', 'skr', 'weight', 'moisture')
    list_filter = ('batch', 'field_officer')
    search_fields = ('batch__batch_number', 'field_officer__name', 'sample_number')

# Unregister ReceivingNormalSKR if it was previously registered without a custom class
try:
    admin.site.unregister(ReceivingNormalSKR)
except admin.sites.NotRegistered:
    pass

# Register ReceivingNormalSKR with its custom admin class
admin.site.register(ReceivingNormalSKR, ReceivingNormalSKRAdmin)


# Register all other models directly
admin.site.register(Batch)
admin.site.register(Region)
admin.site.register(Store)
admin.site.register(FieldOfficer)
admin.site.register(ReceivingSKRWithMoisture)
admin.site.register(ReceivingFOAverage)

