from django.shortcuts import render
from .models import Event


def home(request):
    """
    Display the homepage.
    """
    return render(request, "events/home.html")


def event_list(request):
    """
    Display a list of all published events.
    """
    events = Event.objects.filter(status=1)

    context = {
        "events": events,
    }

    return render(request, "events/event_list.html", context)