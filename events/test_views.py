from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event

class EventListViewTests(TestCase):
    # Arrange: Set up test data for the EventListView tests
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Create a published event and a draft event for testing
        self.published_event = Event.objects.create(
            creator=self.user,
            title="Published Event",
            slug="published-event",
            description="A published event.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            status=1
        )
        
        # Create a draft event to test that it does not appear in the event list view
        self.draft_event = Event.objects.create(
            creator=self.user,
            title="Draft Event",
            slug="draft-event",
            description="A draft event.",
            venue="Private Venue",
            location="Bristol",
            date=timezone.now(),
            genre="Techno",
            status=0
        )
    # Act: Test that the event list view returns a 200 status code and uses the correct template   
    def test_event_list_page_loads(self):
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    # Act: Test that the event list view only displays published events
    def test_event_list_uses_correct_template(self):
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the correct template is used for the event list view
        self.assertTemplateUsed(
            response,
            "events/event_list.html"
        )
    
    # Act: Test that the event list view only shows published events and not draft events    
    def test_event_list_only_shows_published_events(self):
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the published event is in the context and the draft event is not
        self.assertContains(response, "Published Event")
        self.assertNotContains(response, "Draft Event")
        
     # Act: Test that the event list view shows a message when there are no published events   
    def test_event_list_shows_message_when_there_are_no_published_events(self):
        # Delete the published event to simulate no published events
        self.published_event.delete()
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the response contains the message indicating no published events are available
        self.assertContains(response, "No published events are currently available.")
        self.assertNotContains(response, "Draft Event")