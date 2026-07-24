from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context 
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required

# Create your views here.

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
    # a context dictionary to render the template with the events data. Which the template
    # can iterate through to display the events.
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

# Decorator "@login_required" to ensure that only logged-in users can access the event_create view.
@login_required
def event_create(request):
    """
    View for creating a new event. Only accessible to logged-in users.
    """
    # Check if the request method is POST, which indicates that the user has submitted the form.
    if request.method == "POST":
        # Create an instance of the EventForm with the submitted data and files.
        form = EventForm(request.POST, request.FILES)
        # Check if the form is valid (all required fields are filled out correctly).
        if form.is_valid():
            # Save the form but don't commit to the database yet, so we can set the creator field
            event = form.save(commit=False)
            
            # Set the creator of the event to the currently logged-in user
            event.creator = request.user
            
            # Save the event to the database after setting the creator field
            event.save()
            
            # Redirect to the event detail page after successful creation
            return redirect("event_detail", slug=event.slug)
        
    # Else -If the request method is not POST, create a new instance of the EventForm 
    # to display an empty form to the user.
    else:
        form = EventForm()
    # Create a context dictionary to pass the form to the template for rendering
    context = {
        "form": form,
    }
    # Render the event_form.html template with the context containing the form
    return render(request, "events/event_form.html", context)

@login_required
def event_edit(request, slug):
    """
    View for editing an existing event.
    Only the event creator should be able to edit it.
    """
    # Asks the database for the event with the given slug. If no event is found,
    # a 404 error page will be returned.
    event = get_object_or_404(Event, slug=slug)
    
    # This prevents one user from editing another user's event. If the logged-in user 
    # is not the creator of the event, they are redirected to the event detail page 
    # instead of being allowed to edit it. This adds a layer of security to ensure 
    # that only the creator of the event can make changes to it.
    if event.creator != request.user:
        return redirect("event_detail", slug=event.slug)
    
    # Check if the request method is POST, which shows the user has submitted the form.
    if request.method == "POST":
        
        # Create an instance of the EventForm with the submitted data and files
        form = EventForm(
            request.POST,
            request.FILES,
            
            # instance=event tells Django to update the existing Event instance with 
            # the new data from the form instead of creating a new one.
            instance=event,
    )    
        
        # Check if the form is valid (all required fields are filled out correctly).
        if form.is_valid():
            # I used event = form.save() to save the form because the existing event instance 
            # ALREADY has a creator, so it does not need to be set again. The form.save() method 
            # will update the existing event instance with the new data from the form.
            event = form.save()
            
            # Redirect user to the event detail page after successful edit
            return redirect("event_detail", slug=event.slug)
    
    # Else - If the request method is not POST, create an instance of the EventForm with the 
    # existing event data to display the form pre-filled with the current event details.
    else:
        form = EventForm(instance=event)
        
    context = {
        "form": form,
        "event": event,
    }

    return render(request, "events/event_form.html", context)