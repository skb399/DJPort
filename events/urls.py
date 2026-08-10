# Importing the necessary modules and functions from Django. The path function is used to define URL patterns,
from django.urls import path

# Importing the views module from the current package (events) to access the view functions defined in events/views.py.
from . import views

urlpatterns = [
     
# ---------------------------------------------------------------------------
# HOME URL
# ---------------------------------------------------------------------------

    # Add a URL pattern for the home page.
    path(
        # The empty string "" shows that this URL pattern matches the root URL 
        # of the application.
        "",
        views.home,
       # The name parameter is used to uniquely identify this URL pattern,
       # which can be useful for reverse URL matching in templates and views. 
        name="home"),
    
# ---------------------------------------------------------------------------
# EVENT URLS
# ---------------------------------------------------------------------------

    # Add a URL pattern for the event list view, which displays all published events.
    path(
         # Define the URL path used to access the event list view. The "events/" string shows that this URL pattern matches
         # the /events/ URL path.
         "events/", 
         # The views.event_list function is called when this URL pattern is matched.
         views.event_list, 
         # Give the URL pattern a name so it can be referenced
         # in templates and views using Django's URL reversing.
         name="event_list"
         ),
   
    # Add a URL pattern for the event creation view, which is only accessible to logged-in users. 
    # The @login_required decorator in the views ensure that only authenticated users can access 
    # this view.
    path("events/create/", 
         
         # The views.event_create function is called when this URL pattern is matched.
         views.event_create,
         name="event_create"
         ),
    
    # Add a URL pattern for the event edit view, this allows logged-in users to edit an existing event.
    # URL ordering is important in Django, as the first matching pattern will be used, so this needs to go
    # before the event detail view to avoid conflicts. If the event detail view was placed before this,
    # it would match any URL with a slug and prevent access to the event edit view.
    path(
          # Define a URL pattern for the event edit view. The <slug:slug> part of the URL captures the slug of 
          # the event to be edited and passes it as an argument to the view function. The first slug is the data type,
          # and the second slug is the variable name that will be passed to the view function.
          "events/<slug:slug>/edit/", 
               
          # The views.event_edit function is called when this URL pattern is matched.The <slug:slug> part of the URL 
          # captures the slug of the event to be edited, and passes it as an argument to the view function.
          views.event_edit,
          name="event_edit",
     ),
    
    # Adds a URL pattern for the event delete view, which allows logged-in users to delete an existing event.
    # URL ordering is important in Django, as the first matching pattern will be used, so this needs to go before
    # the event detail view to avoid conflicts. If the event detail view was placed before this,
    # it would match any URL with a slug and prevent access to the event delete view.
    path(
    # Define a URL pattern for the event delete view, which allows logged-in users to delete an existing event, the slug 
    # is used to uniquely identify each event in the URL. The first slug is the data type, and the second slug is the variable
    # name that will be passed to the view function. 
    "events/<slug:slug>/delete/",
    
    # The views.event_delete function is called when this URL pattern is matched.
    # The <slug:slug> part of the URL captures the slug of the event to be deleted and passes it as an argument to the view function.
    views.event_delete,
     # The name parameter is used to uniquely identify this URL pattern,
     # which can be useful for reverse URL matching in templates and views.
    name="event_delete",
     ),
    
    # Add a URL pattern for the add comment view, which allows logged-in users to add comments to an event. 
    path(
     # Define a URL pattern for the add comment view
     "events/<slug:slug>/comment/",
     
     # The views.add_comment function is called when this URL pattern is matched.
     views.add_comment,
     
     # The name parameter is used to uniquely identify this URL pattern,
     # which can be useful for reverse URL matching in templates and views.
     name="add_comment",
     ),
    
    # Add a URL pattern for the edit comment view, which allows logged-in users to 
    # edit their own comments on an event.
    path(      
    "comments/<int:comment_id>/edit/",
    views.edit_comment,
    name="edit_comment"
     ),
    
    path(
    # Define a URL pattern for the toggle favourite view    
    "events/<slug:slug>/favourite/",
    
    # The views.toggle_favourite function is called when this URL pattern is matched.
    views.toggle_favourite,
    
    # The name parameter is used to uniquely identify this URL pattern,
    # which can be useful for reverse URL matching in templates and views.
    name="toggle_favourite",
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
     
     # Add a URL pattern for the logged-in user's favourite events page.
     path(
     # Define the URL path used to access the favourite events page 
     "favourites/",
     # The views.favourite_events function is called when this URL pattern is matched.
     views.favourite_events,
     # The name parameter is used to uniquely identify this URL pattern,
     # which can be useful for reverse URL matching in templates and views.
     name="favourite_events",
     ),
# ---------------------------------------------------------------------------
# DJ PROFILE URLS
# ---------------------------------------------------------------------------
     
     # Add a URL pattern for the DJ profile list view, which displays all DJ profiles.
    path("dj-profiles/",
        
        # The views.dj_profile_list function is called when this URL pattern is matched. 
        views.dj_profile_list,
        
        # The name parameter is used to uniquely identify this URL pattern,
        name="dj_profile_list",
    ),    
     
     # Add a URL pattern for the DJ profile creation view. The @login_required decorator in the view ensures 
     # that only authenticated users can access it.
     path(
     
     # The @login_required decorator in the view ensures that only authenticated users can access this view.
     "dj-profiles/create/",
     
     # The views.dj_profile_create function is called when this URL pattern is matched.
     views.dj_profile_create,
     
     # The name parameter is used to uniquely identify this URL pattern,
     # which can be useful for reverse URL matching in templates and views.
     name="dj_profile_create",
     ),
     
    path(
         # Add a URL pattern for the DJ profile detail view, which displays the details of a specific DJ profile.
        "dj-profiles/<slug:slug>/",
        
        # The views.dj_profile_detail function is called when this URL pattern is matched.
        views.dj_profile_detail,
        
        # The name parameter is used to uniquely identify this URL pattern, 
        # which can be useful for reverse URL matching in templates and views.
        name="dj_profile_detail",
    ),

     path(
          
          # Add a URL pattern for the DJ profile edit view, which allows logged-in users to edit an existing DJ profile.
          "dj-profiles/<slug:slug>/edit/",
          
          # The views.dj_profile_edit function is called when this URL pattern is matched.
          views.dj_profile_edit,
          
          # The name parameter is used to uniquely identify this URL pattern,
          # which can be useful for reverse URL matching in templates and views.
          name="dj_profile_edit",
          ),
     
     path(
          # Add a URL pattern for the DJ profile delete view, which allows logged-in users to delete an existing DJ profile.
          "dj-profiles/<slug:slug>/delete/",
          
          # The views.dj_profile_delete function is called when this URL pattern is matched.
          views.dj_profile_delete,
          
          # Give the URL pattern a name so it can be referenced
          # in templates and views using Django's URL reversing.
          name="dj_profile_delete",
          ),
]