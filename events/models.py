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

class DJProfile(models.Model):
    """
    DJ Profile Model for the DJ Port application. This stores a DJ profile linked to one registered user.
    Each user can only create one DJ profile, and the profile includes fields for the DJ's name, bio, 
    genres, location, image, website, and social media links. The model also includes timestamps for when 
    the profile was created and last updated.
    """

    # The owner field is a one-to-one relationship with the User model, ensuring that each user can only 
    # have one DJ profile. owner is used because it represents the user who owns the DJ profile. 
    # The on_delete=models.CASCADE argument ensures that if a user is deleted, their associated 
    # DJ profile will also be deleted. The related_name="dj_profile" allows you to access the DJ 
    # profile from the User model using user.dj_profile.
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="dj_profile"
    )

    # The dj_name field is a CharField that stores the DJ's name, with a maximum length of 100 characters.
    dj_name = models.CharField(max_length=100)

    # The slug field is a SlugField that stores a URL-friendly version of the DJ's name, with a maximum 
    # length of 100 characters. The unique=True argument ensures that each DJ profile has a unique slug, 
    # which is automatically generated from the DJ's name if not provided.
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    # The bio field is a TextField that stores a brief biography or description of the DJ.
    bio = models.TextField()

    # The genres field is a CharField that stores the musical genres associated with the DJ, with a 
    # maximum length of 200 characters. This allows users to specify the types of music they play
    genres = models.CharField(max_length=200)

    # The location field is a CharField that stores the DJ's location, with a maximum length of 100 characters.
    location = models.CharField(max_length=100)

    # The image field is a CloudinaryField that allows users to upload an image for their DJ profile.
    image = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    # The website field is a URLField that stores the DJ's personal or professional website link.
    website = models.URLField(blank=True)

    # The social_media field is a URLField that stores the DJ's social media profile link, allowing
    # users to link to the DJ's social media profiles.
    social_media = models.URLField(blank=True)

    # The created_on field is a DateTimeField that automatically records the date and time when the 
    # DJ profile is created. The auto_now_add=True argument means that the field is set to the current
    # date and time when the profile is first created, and it cannot be changed afterward.
    created_on = models.DateTimeField(auto_now_add=True)

    # The updated_on field is a DateTimeField that automatically records the date and time when the
    # DJ profile is last updated. The auto_now=True argument means that the field is updated whenever
    # the profile is saved, allowing you to track when the profile was last modified.
    updated_on = models.DateTimeField(auto_now=True)

        # The Meta class sets the default ordering of DJ profiles to be in ascending order based on 
        # the dj_name field.
    class Meta:
        ordering = ["dj_name"]

    # The __str__ method provides a human-readable representation of the DJProfile instance, 
    # which is the DJ's name.
    def __str__(self):
        return self.dj_name

    # The save method is overridden to automatically generate a slug from the DJ's name before saving the
    # DJProfile instance to the database. This ensures that each DJ profile has a unique identifier.
    def save(self, *args, **kwargs):
        """
        Generate a slug from the DJ name before saving.
        """
        # If the slug field is empty, generate a slug from the dj_name field using the slugify function.
        if not self.slug:
            self.slug = slugify(self.dj_name)

        # Call the parent class's save method to save the DJProfile instance to the database.
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