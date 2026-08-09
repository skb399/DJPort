from django.shortcuts import get_object_or_404, redirect, render

# Comments not imported because they are not used in this file. The Comment model 
# is only used in the add_comment view, which is already imported from the views module.
from .models import Event, DJProfile
 
from .forms import EventForm, CommentForm, DJProfileForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

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
    
    # Retrieve only approved comments linked to this event.
    comments = event.comments.filter(approved=True)
    
    comment_form = CommentForm()
    
    # The is_favourited variable is calculated in the view because the view is responsible 
    # for preparing data for the template. This keeps the template focused on displaying 
    # the data rather than performing database queries. The template can then simply check 
    # whether is_favourited is True or False to display the correct favourite button.
    if request.user.is_authenticated:
        is_favourited = event.favourited_by.filter(id=request.user.id).exists()
    
    else:
        is_favourited = False

    # Create a context dictionary to pass the event to the template. 
    # This is for a single event, so the key is singular "event" 
    # instead of plural "events" that was used in the event_list view.
    context = {
        "event": event,
        "comments": comments,
        "comment_form": comment_form,
        "is_favourited": is_favourited,
    }

    return render(request, "events/event_detail.html", context)

@login_required
def add_comment(request, slug):
    """
    Allow a logged-in user to submit a comment on an event. 
    """
    # Use get_object_or_404 to retrieve the event with the given slug.
    # If no event is found, a 404 error page will be returned.
    event = get_object_or_404(Event, slug=slug)

    # Check if the request method is POST, which indicates that the user has submitted the comment form.
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        # Check if the form is valid (all required fields are filled out correctly).
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)

            # Link the comment to the selected event. Prevents the user from choosing which event to comment on, 
            # as the comment is automatically linked to the event detail page they are on.
            comment.event = event

            # Link the comment to the currently logged-in user. Prevents the user from choosing which user to 
            # comment as, as the comment is automatically linked to the logged-in user.
            comment.author = request.user

            # Save the comment with approved=False by default.
            comment.save()
    
    # Redirect the user back to the event detail page after submitting the comment.
    return redirect("event_detail", slug=event.slug)

# Decorator "@login_required" to ensure that only logged-in users can access the toggle_favourite view.
@login_required
def toggle_favourite(request, slug):
    """
    Add or remove an event from the logged-in user's favourites. 
    """
    event = get_object_or_404(Event, slug=slug)

    # Check if the request method is POST, confirming that the user has clicked the favourite/unfavourite button.
    if request.method == "POST":
        
        # Check if the logged-in user has already favourited the event.
        if event.favourited_by.filter(id=request.user.id).exists():
            event.favourited_by.remove(request.user)
            messages.success(request, "Event removed from your favourites.")
        
        # If the user has not favourited the event, add them to the favourited_by list.
        else:
            event.favourited_by.add(request.user)
            messages.success(request, "Event added to your favourites.")
   
    # Redirect the user back to the event detail page after toggling the favourite status.
    return redirect("event_detail", slug=event.slug)

# Decorator "@login_required" to ensure that only logged-in users can access the event_create view.
@login_required
def event_create(request):
    """
    View for creating a new event. Only accessible to logged-in users.
    """
    # Check if the request method is POST, which shows that the user has submitted the form.
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

# Decorator "@login_required" to ensure that only logged-in users can access the dj_profile_create view.
@login_required
def dj_profile_create(request):
    """
    View for allowing a logged-in user to create one DJ profile.
    """

    # Prevent a user from creating more than one DJ profile. If a DJ profile already exists for the 
    # logged-in user, they are redirected to the homepage with a warning message.
    if DJProfile.objects.filter(owner=request.user).exists():
        messages.warning(
            request,
            "You already have a DJ profile."
        )
        return redirect("home")

    # Check if the request method is POST, showing that the user
    # has submitted the DJ profile form. 
    if request.method == "POST":
        form = DJProfileForm(
            request.POST,
            request.FILES
        )

        # Check that all required form fields are valid. 
        if form.is_valid():
            # Save the form without committing it to the database yet, if it was committed now, the 
            # owner field would be empty and cause an error.
            profile = form.save(commit=False)

            # Automatically assign the logged-in user as the owner, so they cannot create a DJ profile 
            # for someone else.
            profile.owner = request.user

            # Save the completed DJ profile to the database.
            profile.save()
            
            # Display a success message to the user after successfully creating their DJ profile.
            messages.success(
                request,
                "Your DJ profile has been created successfully."
            )

            # Redirect the user to the homepage after successfully creating their DJ profile.
            return redirect("home")

    # Else - If the request method is not POST, create a new instance of the DJProfileForm to display
    # an empty form to the user.
    else:
        form = DJProfileForm()

    # Create a context dictionary to pass the form to the template for rendering
    context = {
        "form": form,
    }

    # Render the dj_profile_form.html template with the context containing the form
    return render(
        request,
        "events/dj_profile_form.html",
        context
    )

# Decorator "@login_required" to ensure that only logged-in users can access the event_edit view.
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
            # already has a creator, so it does not need to be set again. The form.save() method 
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

# Decorator "@login_required" to ensure that only logged-in users can access the event_delete view.
@login_required
def event_delete(request, slug):
    """
    Allow an event creator to delete their own event.
    """
    # Retrieve the requested event or return a 404 page if it does not exist.
    event = get_object_or_404(Event, slug=slug)

    # Prevent logged-in users from deleting events created by someone else. This has been recycled 
    # from the event_edit view to ensure that only the creator of the event can delete it.
    if event.creator != request.user:
        return redirect("event_detail", slug=event.slug)

    # Only delete the event after the confirmation form is submitted. This has also been recycled 
    # from the event_edit view to ensure that the event is only deleted after the user confirms.
    if request.method == "POST":
        event.delete()

        # The deleted event no longer has a usable detail page,
        # so redirect the user to the event list.
        return redirect("event_list")

    context = {
        "event": event,
    }

    # A GET request displays the confirmation page.
    return render(request, "events/event_confirm_delete.html", context)

# -----------------------------------------------------------------------------------------------------
# DJ PROFILE VIEWS
#------------------------------------------------------------------------------------------------------

def dj_profile_list(request):
    """
    Display a list of all DJ profiles.
    """
    # Retrieve all DJ profiles. Filter not required as DJ profiles don't have draft or published status
    dj_profiles = DJProfile.objects.all()

    # Create a context dictionary to pass the DJ profiles to the template as Django needs 
    # a context dictionary to render the template with the DJ profiles data. Which the template
    # can iterate through to display the DJ profiles.
    context = {
        "dj_profiles": dj_profiles,
    }

    return render(request, "events/dj_profile_list.html", context)

def dj_profile_detail(request, slug):
    """
    Display the details of a specific DJ profile based on its slug.
    """
    # Retrieve the DJ profile with the matching slug.
    # If no profile is found, return a 404 page.
    dj_profile = get_object_or_404(DJProfile, slug=slug)

    # Create a context dictionary to pass the DJ profile to the template as Django needs 
    # a context dictionary to render the template with the DJ profile data. Which the template
    # can use to display the DJ profile details.
    context = {
        "dj_profile": dj_profile,
    }

    # Render the dj_profile_detail.html template with the context containing the DJ profile
    return render(
        request,
        "events/dj_profile_detail.html",
        context
    )

# Decorator "@login_required" to ensure that only logged-in users can access the dj_profile_edit view.
@login_required
def dj_profile_edit(request, slug):
    """
    Allow a DJ profile owner to edit their own profile.
    """
    # Retrieve the DJ profile with the matching slug. If no profile is found, return a 404 page.
    dj_profile = get_object_or_404(DJProfile, slug=slug)

    # Prevent users from editing another user's DJ profile. If the logged-in user is not the owner of the DJ profile,
    # they are redirected to the DJ profile detail page instead of being allowed to edit it.
    if dj_profile.owner != request.user:
        return redirect(
            "dj_profile_detail",
            slug=dj_profile.slug
        )

    # Check if the request method is POST, which indicates that the user has submitted the form.
    if request.method == "POST":
        
        # Reuse the DJProfileForm with the existing DJ profile instance,
        # allowing the user to update their current profile details.
        form = DJProfileForm(
            request.POST,
            request.FILES,
            instance=dj_profile
        )
        
        # Check if the form is valid (all required fields are filled out correctly).
        if form.is_valid():
            dj_profile = form.save()

            messages.success(
                request,
                "Your DJ profile has been updated successfully."
            )

            # Redirect the user to the DJ profile detail page after successfully editing their DJ profile.
            return redirect(
                "dj_profile_detail",
                slug=dj_profile.slug
            )

    # Else - If the request method is not POST, create an instance of the DJProfileForm with the existing 
    # DJ profile data to display the form pre-filled with the current DJ profile details.
    else:
        # Reuse the DJProfileForm with the existing DJ profile instance
        # to display the user's current profile details in the form.
        form = DJProfileForm(instance=dj_profile)

    # Create a context dictionary to pass the form and DJ profile to the template for rendering 
    context = {
        "form": form,
        "dj_profile": dj_profile,
    }
    
    # Render the dj_profile_form.html template with the context containing the form and DJ profile
    return render(
        request,
        "events/dj_profile_form.html",
        context
    )

# Decorator "@login_required" to ensure that only logged-in users can access the dj_profile_delete view.
@login_required
def dj_profile_delete(request, slug):
    """
    Allow a DJ profile owner to delete their own profile.
    """
    
    # Retrieve the DJ profile with the matching slug. If no profile is found, return a 404 page.
    dj_profile = get_object_or_404(DJProfile, slug=slug)

    # If the logged-in user is not the owner of the DJ profile,
    # they are redirected to the DJ profile detail page instead of being allowed to delete it.
    if dj_profile.owner != request.user:
        return redirect(
            "dj_profile_detail",
            slug=dj_profile.slug
        )

    # If the request method is POST, delete the DJ profile and redirect the user to the DJ 
    # profile list page with a success message. So the DJ profile is only deleted after the 
    # user confirms the deletion.
    if request.method == "POST":
        dj_profile.delete()

        messages.success(
            request,
            "Your DJ profile has been deleted successfully."
        )

        return redirect("dj_profile_list")

    # If the request method is GET, display the confirmation page to the user before 
    # deleting the DJ profile.
    context = {
        "dj_profile": dj_profile,
    }

    # Render the dj_profile_confirm_delete.html template with the context containing the DJ profile
    return render(
        request,
        "events/dj_profile_confirm_delete.html",
        context
    )