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
    def setUp(self):
        """
        Create a test user and a test event.

        The setUp() method runs before every test, so each test
        starts with a fresh database containing this data.
        """

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

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

    def test_event_string_method_returns_title(self):
        """
        Test that the Event model's __str__ method
        returns the event title.
        """

        self.assertEqual(
            str(self.event),
            "Test Event",
            msg="Event string method does not return the title"
        )

    def test_default_status_is_draft(self):
        """
        Test that a created event thats just been created defaults
        to Draft status when no status is supplied.
        """

        draft_event = Event.objects.create(
            creator=self.user,
            title="Draft Event",
            slug="draft-event",
            description="Draft description",
            venue="Draft Venue",
            location="Bristol",
            date=timezone.now() + timedelta(days=14),
            genre="Techno"
        )

        self.assertEqual(
            draft_event.status,
            0,
            msg="Event status does not default to Draft"
        )

    def test_creator_relationship(self):
        """
        Test that the creator ForeignKey correctly
        links the event to the user who created it.
        """

        self.assertEqual(
            self.event.creator,
            self.user,
            msg="Event is not linked to the correct creator"
        )

    def test_lineup_can_be_blank(self):
        """
        Test that the lineup field has optional entry for the user.

        If no lineup is provided, Django should
        store an empty string.
        """

        self.assertEqual(
            self.event.lineup,
            "",
            msg="Lineup field does not allow blank values"
        )