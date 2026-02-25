from django.contrib import admin
from profiles.models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    # Admin configuration for Profile model

    # Columns visible in list view
    list_display = (
        "id",
        "user",
        "location",
        "created_at",
    )

    # Add search functionality
    search_fields = (
        "user__email",
        "user__username",
        "location",
    )

    # Filters on right sidebar
    list_filter = (
        "location",
        "created_at",
    )

    # Default ordering
    ordering = ("-created_at",)

    # Make certain fields read-only
    readonly_fields = ("created_at",)