from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Event


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
        # Assert: Check that the string representation of the event is its title
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
        # Assert: Check that the default status of the new event is Published (1)
        self.assertEqual(
            published_event.status,
            1,
            msg="Event status should default to Published"
        )

    # Test that the creator ForeignKey correctly links the event to the user who created it
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
        # Assert: Check that the lineup field is an empty string when not provided
        self.assertEqual(
            self.event.lineup,
            "",
            msg="Lineup field does not allow blank values"
        )