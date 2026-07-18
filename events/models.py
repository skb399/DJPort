from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


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
        default=0
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