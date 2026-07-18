from django.shortcuts import get_object_or_404, render
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
    # Filter events to only include those with a status of 1 (Published)
    events = Event.objects.filter(status=1)

    # Create a context dictionary to pass the events to the template as Django needs 
    # a context dictionary to render the template with the events data.
    context = {
        "events": events,
    }

    return render(request, "events/event_list.html", context)

def event_detail(request, slug):
    """
    Display the details of a specific event based on its slug.
    """
    # Use get_object_or_404 to retrieve the event with the given slug.
    # If no event is found, a 404 error page will be returned.    
    event = get_object_or_404(Event, slug=slug)

    # Create a context dictionary to pass the event to the template. 
    # This is for a single event, so the key is singular "event" 
    # instead of plural "events" that was used in the event_list view.
    context = {
        "event": event,
    }

    return render(request, "events/event_detail.html", context)