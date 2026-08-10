from django.contrib import admin
from .models import Event, Comment, DJProfile


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Customises how events are displayed and managedin the Django admin panel. 
    A good reason to have an EventAdmin class is to customise how events are managed 
    in Django Admin, like filtering, searching, and displaying 
    specific information about events. This can help administrators 
    manage user-generated content and maintain events on the site.
    """
    
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
    in the Django admin panel. A good eason to have 
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
    
@admin.register(DJProfile)
class DJProfileAdmin(admin.ModelAdmin):
    """
    Customises how DJ profiles are displayed and managed in the Django admin panel. A good reason
    to have a DJProfileAdmin class is to customise how DJ profiles are managed in Django Admin, 
    such as filtering, searching, and displaying relevant information about DJ profiles. 
    This can help administrators manage user-generated content and maintain DJ profiles on the site.
    """

    # Display useful DJ profile information in the admin list view.
    list_display = (
        "dj_name",
        "owner",
        "location",
        "created_on",
        "updated_on",
    )

    # Allow administrators to filter DJ profiles by location
    # and creation date.
    list_filter = (
        "location",
        "created_on",
    )

    # Allow administrators to search DJ profiles by DJ name,
    # owner's username, genres, or location.
    search_fields = (
        "dj_name",
        "owner__username",
        "genres",
        "location",
    )

    # Automatically populate the slug field from the DJ name
    # when creating a DJ profile through Django Admin.
    prepopulated_fields = {
        "slug": ("dj_name",)
    }