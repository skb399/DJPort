from django import forms
from .models import Event



class EventForm(forms.ModelForm):
    """
    Form for logged-in users to create and edit events.
    """

    # Meta class to specify the model and fields to be used in the form, creator, 
    # slug and status not included as they are automatically set in the view and
    # not meant to be edited by the user.
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "venue",
            "location",
            "date",
            "genre",
            "lineup",
            "featured_image",
        ]
        # Used a widget to customise the date input field to use a datetime-local input type,
        # which allows users to select both date and time in a single input field. The format
        # is set to match the expected input format for this type of field.
        widgets = {
            "date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        
    # The __init__ method is overridden to set the input format for the date field to match
    # the format used by the datetime-local input type. This ensures that the form can correctly
    # parse and validate the date input from the user.
    def __init__(self, *args, **kwargs):
        # Call the parent class's __init__ method to ensure that the form is initialized properly
        super().__init__(*args, **kwargs)

        # Accept the format submitted by the datetime-local HTML input.
        self.fields["date"].input_formats = ["%Y-%m-%dT%H:%M"]