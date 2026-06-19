from django.contrib import admin

from .models import PI


@admin.register(PI)
class PIAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'relationship',
        'building',
        'unit',
        'room',
        'property_type',
    )
    search_fields = ('name', 'phone', 'building', 'unit', 'room')
    list_filter = ('relationship', 'building', 'unit', 'property_type')
