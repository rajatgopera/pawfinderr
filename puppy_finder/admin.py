from django.contrib import admin
from .models import Puppy

@admin.register(Puppy)
class PuppyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'status',
        'get_owner_username',
        'last_seen_date',
        'contact_name',
        'contact_email'
    )
    search_fields = [
        'name',
        'created_by__username',
        'contact_email',
        'microchip_number'
    ]
    list_filter = (
        'status',
        'last_seen_date',
    )
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'status')
        }),
        ('Owner Details', {
            'fields': ('created_by', 'contact_name', 'contact_email')
        }),
        ('Identification', {
            'fields': ('microchip_number', 'collar_description')
        }),
        ('Dates', {
            'fields': ('last_seen_date',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'additional_notes'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')

    def get_owner_username(self, obj):
        return obj.created_by.username if obj.created_by else None
    get_owner_username.short_description = 'Owner'

# Register your models here.
