from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Event, DJProfile, Comment

# Some testing patterns in this file were informed by the
# Code Institute Codestar Blog walkthrough project.
# Tests have been adapted and expanded for DJ Port's models
# and application-specific behaviour.

class TestEventModel(TestCase):
    """
    Tests for the Event model.
    These tests check that the model works as expected.
    """

    # self refers to the instance that has been called by the class. It allows
    # methods to access data stored in that object, like the
    # test user and test event created in setUp(). Using self
    # means the same objects can be reused across multiple test
    # methods without recreating them.

    # Arrange: Set up test data for the Event model tests
    def setUp(self):
        """
        Create a test user and a test event.

        The setUp() method runs before every test, so each test
        starts with a fresh database containing this data.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create a test event with the test user as the creator
        self.event = Event.objects.create(
            creator=self.user,
            title="Test Event",
            slug="test-event",
            description="Test description",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now() + timedelta(days=7),
            genre="House",
            status=1
        )

    # Test that the Event model's __str__ method returns the event title
    def test_event_string_method_returns_title(self):
        """
        Test that the Event model's __str__ method
        returns the event title.
        """
        # Assert: Check that the string representation of the event is its
        # title
        self.assertEqual(
            str(self.event),
            "Test Event",
            msg="Event string method does not return the title"
        )

    # Test that a newly created event defaults to Published (1).
    def test_default_status_is_published(self):
        """
        Test that a created event that's just been created defaults
        to Published status.
        """
        # Create a new event without specifying the status
        published_event = Event.objects.create(
            creator=self.user,
            title="Published Event",
            slug="published-event",
            description="Published description",
            venue="Published Venue",
            location="Bristol",
            date=timezone.now() + timedelta(days=14),
            genre="Techno"
        )
        # Assert: Check that the default status of the new event is Published
        # (1)
        self.assertEqual(
            published_event.status,
            1,
            msg="Event status should default to Published"
        )

    # Test that the creator ForeignKey correctly links the event to the user
    # who created it
    def test_creator_relationship(self):
        """
        Test that the creator ForeignKey correctly
        links the event to the user who created it.
        """
        # Assert: Check that the event's creator is the test user
        self.assertEqual(
            self.event.creator,
            self.user,
            msg="Event is not linked to the correct creator"
        )

    # Test that the lineup field can be left blank
    def test_lineup_can_be_blank(self):
        """
        Test that the lineup field has optional entry for the user.

        If no lineup is provided, Django should
        store an empty string.
        """
        # Assert: Check that the lineup field is an empty string when not
        # provided
        self.assertEqual(
            self.event.lineup,
            "",
            msg="Lineup field does not allow blank values"
        )


class DJProfileModelTests(TestCase):
    """
    Tests for the DJProfile model.
    """

    def setUp(self):
        """
        Create users and a DJ profile for use in the tests.
        """
        # Arrange: Create a user who will own the first DJ profile.
        self.user = User.objects.create_user(
            username="djuser",
            password="testpassword"
        )

        # Arrange: Create a second user so we can test that two different
        # users can use the same DJ name without causing a duplicate slug
        # error.
        self.other_user = User.objects.create_user(
            username="otherdjuser",
            password="testpassword"
        )

        # Arrange: Create a DJ profile that can be reused throughout the tests.
        # The slug is not provided so the model should create it automatically
        # from the DJ name when the profile is saved.
        self.dj_profile = DJProfile.objects.create(
            owner=self.user,
            dj_name="DJ Pulse",
            bio="Test DJ profile.",
            genres="House",
            location="Manchester"
        )

    def test_dj_profile_string_returns_dj_name(self):
        """
        Test that the string representation returns the DJ name.
        """
        # Assert: Check that converting the DJ profile to a string returns
        # the DJ name, making the profile easy to identify in Django admin.
        self.assertEqual(str(self.dj_profile), "DJ Pulse")

    def test_slug_is_created_from_dj_name(self):
        """
        Test that a slug is automatically generated from the DJ name.
        """
        # Assert: Check that the model has converted "DJ Pulse" into the
        # URL-friendly slug "dj-pulse" when the profile was created.
        self.assertEqual(self.dj_profile.slug, "dj-pulse")

    def test_duplicate_dj_names_create_unique_slugs(self):
        """
        Test that profiles with the same DJ name receive unique slugs.
        """
        # Arrange: Create another DJ profile with the same DJ name.
        # This uses a different user because each user can only own one
        # DJ profile due to the OneToOneField relationship.
        second_profile = DJProfile.objects.create(
            owner=self.other_user,
            dj_name="DJ Pulse",
            bio="Another test DJ profile.",
            genres="Techno",
            location="Liverpool"
        )

        # Assert: The first profile keeps the original slug.
        self.assertEqual(self.dj_profile.slug, "dj-pulse")

        # Assert: The second profile is given a numbered slug so that the
        # unique slug constraint does not cause a database error.
        self.assertEqual(second_profile.slug, "dj-pulse-2")

        # Assert: Confirm that both profiles have different slugs even though
        # they use the same DJ name.
        self.assertNotEqual(
            self.dj_profile.slug,
            second_profile.slug
        )

    def test_slug_does_not_change_when_profile_is_edited(self):
        """
        Test that editing the DJ name does not change the existing slug.
        """
        # Arrange: Store the original slug before editing the profile.
        original_slug = self.dj_profile.slug

        # Act: Change the DJ name and save the existing profile.
        self.dj_profile.dj_name = "DJ Pulse Updated"
        self.dj_profile.save()

        # Assert: Check that the original slug has been kept.
        # This prevents the DJ profile URL from changing after an edit.
        self.assertEqual(self.dj_profile.slug, original_slug)


class CommentModelTests(TestCase):
    """
    Tests for the Comment model.
    """

    def setUp(self):
        """
        Create users, an event and a comment for use in the tests.
        """
        # Arrange: Create a user who will own the event.
        self.event_owner = User.objects.create_user(
            username="eventowner",
            password="testpassword"
        )

        # Arrange: Create another user who will write the comment.
        self.comment_author = User.objects.create_user(
            username="commentauthor",
            password="testpassword"
        )

        # Arrange: Create an event for the comment to be attached to.
        self.event = Event.objects.create(
            creator=self.event_owner,
            title="Test Event",
            description="A test event.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House"
        )

        # Arrange: Create a comment without setting the approved field.
        # This allows us to check that new comments require approval by
        # default.
        self.comment = Comment.objects.create(
            event=self.event,
            author=self.comment_author,
            body="This is a test comment."
        )

    def test_comment_is_not_approved_by_default(self):
        """
        Test that a new comment is not approved by default.
        """
        # Assert: Check that the approved field is False when a comment
        # is first created, so it must be moderated before being displayed.
        self.assertFalse(self.comment.approved)

    def test_comment_string_representation(self):
        """
        Test that the string representation identifies the comment.
        """
        # Assert: Check that converting the comment to a string includes
        # both the comment author's username and the event title.
        self.assertEqual(
            str(self.comment),
            "Comment by commentauthor on Test Event"
        )
