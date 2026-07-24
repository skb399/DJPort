# Importing the necessary modules and functions from Django. The path function is used to define URL patterns,
from django.urls import path

# Importing the views module from the current package (events) to access the view functions defined in events/views.py.
from . import views


urlpatterns = [
    # Add a URL pattern for the home page.
    path(
        # The empty string "" shows that this URL pattern matches the root URL 
        # of the application.
        "",
        views.home,
       # The name parameter is used to uniquely identify this URL pattern,
       # which can be useful for reverse URL matching in templates and views. 
        name="home"),
    
    # Add a URL pattern for the event list view, which displays all published events.
    path("events/", 
         # The views.event_list function is called when this URL pattern is matched.
         views.event_list, 
         # The name parameter is used to uniquely identify this URL pattern,
         # which can be useful for reverse URL matching in templates and views.
         name="event_list"),
   
    # Add a URL pattern for the event creation view, which is only accessible to logged-in users. 
    # The @login_required decorator in the view ensures that only authenticated users can access 
    # this view.
    path("events/create/", 
         
         # The views.event_create function is called when this URL pattern is matched.
         views.event_create,
         
         # The name parameter is used to uniquely identify this URL pattern,
         # which can be useful for reverse URL matching in templates and views.
         name="event_create"),
    
    # Add a URL pattern for the event edit view, this allows logged-in users to edit an existing event.
    # URL ordering is important in Django, as the first matching pattern will be used, so this needs to go
    # before the event detail view to avoid conflicts. If the event detail view was placed before this,
    # it would match any URL with a slug and prevent access to the event edit view.
    path("events/<slug:slug>/edit/", 
   
    # The views.event_edit function is called when this URL pattern is matched. 
    # The <slug:slug> part of the URL captures the slug of the event to be edited
    # and passes it as an argument to the view function.
    views.event_edit,
   
    # The name parameter is used to uniquely identify this URL pattern,
    # which can be useful for reverse URL matching in templates and views.
    name="event_edit",
    ),
    
    # Add a URL pattern for the event detail view. For <slug:slug> - Slug is used to uniquely 
    # identify each event in the URL. The first slug is the data type, and the second slug 
    # is the variable name that will be passed to the view function.
    path("events/<slug:slug>/",
         
         # The views.event_detail function is called when this URL pattern is matched.
         views.event_detail, 
         
         # The name parameter is used to uniquely identify this URL pattern,
         # which can be useful for reverse URL matching in templates and views.
         name="event_detail"),
]