from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("events/", views.event_list, name="event_list"),
    # Add a URL pattern for the event detail view. For <slug:slug> - Slug is used to uniquely 
    # identify each event in the URL. The first slug is the data type, and the second slug 
    # is the variable name that will be passed to the view function.
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
]