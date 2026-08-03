from django.contrib import admin
from .models import Event, Comment


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
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Customises how comments are displayed and managed
    in the Django admin panel. A good reason reason to have 
    a CommentAdmin class is to customise how comments are managed 
    in Django Admin, such as filtering, searching, and displaying 
    relevant information about comments. This can help administrators 
    manage user-generated content and maintain discussions on the site.
    """

    # The list_display attribute specifies the fields to be displayed 
    # in the list view of comments in the admin panel.
    list_display = (
        "author",
        "event",
        "created_on",
        "approved",
    )

    # The list_filter attribute adds filters in the admin panel to
    # allow administrators to filter comments based on their approval status
    list_filter = (
        "approved",
        "created_on",
    )

    # The search_fields attribute enables a search box in the admin panel 
    # to search comments based on the author's username, the event's title, or the comment body.
    search_fields = (
        "author__username",
        "event__title",
        "body",
    ) 