from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


STATUS = (
    (0, "Draft"),
    (1, "Published"),
)



class Event(models.Model):
    """
Event model for the DJ Port application. This model represents an event created by a user,
with fields for the event's title, description, venue, location, date, genre, lineup, and 
status (draft or published). The model also includes a foreign key to the User model to
link the event with its creator, in addition to a many-to-many relationship with the User 
model to allow users to favorite events. The model includes timestamps for when the
event was created and last updated.
    """
    
    #fields for the Event model
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    lineup = models.TextField(blank=True)
    featured_image = CloudinaryField(
    "image",
    # Allows user to submit an event without an image
    blank=True,
    #Means that the database may not store an image value for an event, and the field can be left empty
    null=True
    )
    # status field to indicate whether the event is a draft or published
    status = models.IntegerField(
        choices=STATUS,
        default=1
    )
    venue = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    genre = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    favourited_by = models.ManyToManyField(
    User,
    related_name="favourite_events",
    blank=True
)

    class Meta:
        ordering = ["date"]
    
    def __str__(self):
        return self.title
    
    # The save method is overridden to automatically generate a slug from the event title before 
    # saving the event instance to the database. So that each event has a unique identifier based
    # on its title.
    def save(self, *args, **kwargs):
        """
        Generate a slug from the event title before saving.
        """
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
        

class Comment(models.Model):
    """
    Stores a comment made by a user on an event.

    Each comment is linked to one event and one registered user.
    Comments require approval before they are displayed publicly.
    """
    # The event field is a foreign key to the Event model, setting a many-to-one relationship
    # where multiple comments can be associated with a single event. The on_delete=models.CASCADE 
    # argument ensures that if an event is deleted, all associated comments are also deleted.
    # related_name="comments" allows you to access all comments for an event through event.comments.all()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # The author field is a foreign key to the User model, establishing a many-to-one relationship
    # where multiple comments can be made by a single user. The on_delete=models.CASCADE argument
    # ensures that if a user is deleted, all their comments are also deleted. 
    # The related_name="event_comments" lets you access all comments by a user through user.event_comments.all().
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="event_comments"
    )

    # The body field stores the content of the comment. A TextField is used
    # because it allows users to write comments of varying length without
    # requiring a fixed maximum number of characters.
    body = models.TextField()

    # The created_on field automatically records the date and time when the comment is created. 
    # auto_now_add=True means that the field is set to the current date and time when the comment
    # is first created, and it cannot be changed afterward.
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    # The approved field is a BooleanField that indicates whether the comment has been approved for
    # display. By default, it is set to False, meaning that comments require approval before they 
    # are visible to the public. This allows event organizers or moderators to review comments 
    # before they are displayed.
    approved = models.BooleanField(
        default=False
    )

    # The Meta class sets the default ordering of comments to be in ascending order based on the 
    # created_on field, so that newest comments appear first.
    class Meta:
        ordering = ["-created_on"]

    # The __str__ method provides a human-readable representation of the Comment instance,
    # which includes the author's username and the title of the event the comment is for.
    def __str__(self):
        return f"Comment by {self.author} on {self.event}"