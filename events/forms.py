from django import forms
from .models import Comment, Event



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

        # Accept the format submitted by the datetime-local HTML input
        self.fields["date"].input_formats = ["%Y-%m-%dT%H:%M"]
        
class CommentForm(forms.ModelForm):
    """
    Form for logged-in users to submit comments on events. This is better than manually writing 
    the <textarea> because Django will handle the form rendering, validation, and error handling for you. 
    It also allows you to easily customize the form fields and their attributes using the Meta class and widgets.
    The form is linked to the Comment model, and only the body field is included in the form, as the author and 
    event fields are automatically set in the view and not meant to be edited by the user.  
    """

    # Meta class to specify the model and fields to be used in the form. 
    # The body field is the only field that users can fill out when 
    # submitting a comment, as the author and event fields are automatically
    # set in the view and not meant to be edited by the user.
    class Meta:
        model = Comment
        fields = ["body"]

        # The widgets attribute is used to customise the appearance and behaviour of the form fields.
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Add a comment...",
                }
            ),
        }

        # The labels attribute is used to specify custom labels for the form fields. In this case,
        # the body field is given a custom label "Add a comment:" to provide a clear instruction 
        # to the user about what they should enter in the field. 
        labels = {
            "body": "Add a comment:",
        }