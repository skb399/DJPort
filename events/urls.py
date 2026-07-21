from django.urls import path
from . import views


urlpatterns = [
    # Add a URL pattern for the home page.
    path("", views.home, name="home"),
    
    # Add a URL pattern for the event list view, which displays all published events.
    path("events/", views.event_list, name="event_list"),
   
    # Add a URL pattern for the event creation view, which is only accessible to logged-in users. 
    # The @login_required decorator in the view ensures that only authenticated users can access 
    # this view.
    path("events/create/", views.event_create, name="event_create"),
    
    # Add a URL pattern for the event detail view. For <slug:slug> - Slug is used to uniquely 
    # identify each event in the URL. The first slug is the data type, and the second slug 
    # is the variable name that will be passed to the view function.
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
]