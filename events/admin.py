from django.contrib import admin
from .models import Event

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "creator",
        "venue",
        "location",
        "date",
        "status",
    )

    list_filter = (
        "status",
        "date",
        "genre",
        "location",
    )

    search_fields = (
        "title",
        "venue",
        "location",
        "genre",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }