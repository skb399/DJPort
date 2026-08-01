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
                
    
class EventDetailViewTests(TestCase):
    # Arrange: Set up test data for the EventDetailView tests
    def setUp(self):
        # Create a test user 
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create a published event for testing the event detail view
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
        
        # Create a second published event to test that the event detail 
        # view correctly retrieves the right event based on the slug
        self.other_event = Event.objects.create(
            creator=self.user,
            title="Another Event",
            slug="another-event",
            description="A different event.",
            venue="Another Venue",
            location="London",
            date=timezone.now(),
            genre="Drum & Bass",
            status=1,
        )
    # Act: Test that the event detail page returns a 200 response and 
    # uses the correct template for a valid event    
    def test_event_detail_page_loads_successfully_for_valid_event(self):
        """
        Test that the event detail page returns a 200 response
        and uses the correct template for a valid event.
        """
        # Act: Make a GET request to the event detail view for the published event
        response = self.client.get(
            reverse("event_detail", args=[self.published_event.slug])
        )
        
        # Assert: Check that the response status code is 200 (OK) and the correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_detail.html")
    
    # Act: test that the correct event information appears on the detail page    
    def test_event_detail_displays_correct_event_information(self):
        """
        Test that the event detail page displays the correct event information.
        """
        # Act: Make a GET request to the event detail view for the published event
        response = self.client.get(
            reverse("event_detail", args=[self.published_event.slug])
        )
        # Assert: Check that the response contains the event's title, venue, location, description, and genre
        self.assertContains(response, self.published_event.title)
        self.assertContains(response, self.published_event.venue)
        self.assertContains(response, self.published_event.location)
        self.assertContains(response, self.published_event.description)
        self.assertContains(response, self.published_event.genre)
    
    # Act: Test that the event detail view returns a 404 response for an invalid slug
    def test_event_detail_returns_404_for_invalid_slug(self):
        """
        Test that the event detail view returns a 404 response
        for an invalid slug.
        """
        # Act: Make a GET request to the event detail view with a slug that does not exist
        response = self.client.get(
            reverse("event_detail", args=["event-does-not-exist"])
        )

        # Assert: Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)
    
    # Act: Test that the event detail page only displays the requested event and not other incorrect events
    def test_event_detail_does_not_display_another_event(self):
        """
        Test that the event detail page only displays the requested event.
        """
        # Act: Make a GET request to the event detail view for the published event
        response = self.client.get(
            reverse("event_detail", args=[self.published_event.slug])
        )
        # Assert: Check that the response does not contain information from the other event
        self.assertNotContains(response, self.other_event.title)
        self.assertNotContains(response, self.other_event.venue)
        self.assertNotContains(response, self.other_event.location)
        self.assertNotContains(response, self.other_event.description)
        self.assertNotContains(response, self.other_event.genre)
        
        
class EventCreateViewTests(TestCase):
    """
    Tests for the event_create view.
    """
    # Arrange: Set up test data for the EventCreateView tests
    def setUp(self):
        """
        Create a test user and store the create-event URL.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        # Store the URL for the event creation page using Django's reverse function
        # which allows us to refer to the URL by its name instead of hardcoding it.
        self.create_url = reverse("event_create")

    def test_logged_in_user_can_access_event_create_page(self):
        """
        Test that a logged-in user can access the event creation page.
        """
        # Arrange: Log the test user in
        self.client.login(
            username="testuser",
            password="testpassword"
        )

        # Act: Request the event creation page, which should be accessible to logged-in users
        response = self.client.get(self.create_url)

        # Assert: The page loads and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_form.html")

    def test_logged_out_user_is_redirected_from_event_create_page(self):
        """
        Test that a logged-out user cannot access the event creation page.
        """
        # Act: Request the protected page without logging in, the user should be redirected to the login page
        response = self.client.get(self.create_url)

        # Assert: The user is redirected to the login page, with a 302 status code and the correct redirect URL
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={self.create_url}"
        )
        
    def test_logged_in_user_can_create_event(self):
        """
        Test that a logged-in user can submit valid data
        and create a new event.
        """
        # Arrange: Log the user in
        self.client.login(
            username="testuser",
            password="testpassword"
        )

        # Arrange: Prepare valid form data for creating a new event. 
        # The date is set to a future date to ensure it's valid.
        form_data = {
            "title": "Test Club Night",
            "description": "A test event created through the form.",
            "venue": "Test Venue",
            "location": "Manchester",
            "date": "2026-08-15T22:00",
            "genre": "House",
            "lineup": "DJ Test",
            # featured_image is optional, so I left it out for this test.
        }

        # Act: Submit the form, which should create a new event and 
        # redirect to the event detail page
        response = self.client.post(
            self.create_url,
            data=form_data
        )

        # Assert: One event was created, and the event's details match the submitted data
        self.assertEqual(Event.objects.count(), 1)

        # Retrieve the created event so we can inspect it. There are no events created in this tests'
        # setUp, so after the post there should be exactly one event in the database, which we can retrieve with get().
        created_event = Event.objects.get()

        # Assert: The view assigned the logged-in user as creator
        self.assertEqual(created_event.creator, self.user)

        # Assert: The submitted title was saved, and the event's title matches the form data
        self.assertEqual(created_event.title, "Test Club Night")

        # Assert: The user was redirected to the new event detail page
        self.assertRedirects(
            response,
            # Use reverse to get the URL for the event detail page, passing the slug of the created event as an argument
            reverse(
                "event_detail",
                # Use the slug of the created event to generate the correct URL for the detail view
                args=[created_event.slug]
            )
        )
    def test_invalid_form_does_not_create_event(self):
        """
        Test that invalid form data does not create an event
        and redisplays the event form.
        """
        # Arrange: Log the user in
        self.client.login(
            username="testuser",
            password="testpassword"
        )

        # Arrange: Submit form data without the required title
        invalid_form_data = {
            # Title is required, so leaving it blank should trigger a validation error
            "title": "",
            "description": "An event without a title.",
            "venue": "Test Venue",
            "location": "Manchester",
            "date": "2026-08-15T22:00",
            "genre": "House",
            "lineup": "DJ Test",
        }

        # Act: Submit the invalid form
        response = self.client.post(
            self.create_url,
            data=invalid_form_data
        )

        # Assert: No event was saved, this proves that the invalid submission did not create affect the database, 
        # and the event count remains zero
        self.assertEqual(Event.objects.count(), 0)

        # Assert: This proves that the user stays on the event creation page and sees the form again, 
        # with validation errors displayed, instead of being redirected to another page. 
        # The response status code is 200, indicating that the form was redisplayed, and the correct template is used.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_form.html")
        
        self.assertFormError(
        response.context["form"],
        "title",
        "This field is required."
        )
        
class EventEditViewTests(TestCase):
    """
    Tests for the event_edit view.
    """
    # Arrange: Set up test data for the EventEditView tests
    def setUp(self):
        """
        Create an event owner, another user, an existing event,
        and store the event-edit URL.
        """
        self.owner = User.objects.create_user(
            username="eventowner",
            password="testpassword"
        )
        # other user created to test that only the event owner can edit the event
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword"
        )
        # Create an event owned by the event owner user to be used in the edit tests
        self.event = Event.objects.create(
            creator=self.owner,
            title="Original Event",
            slug="original-event",
            description="The original event description.",
            venue="Original Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            lineup="Original DJ",
            status=1
        )
        # Store the URL for the event edit page using Django's reverse function.
        # This allows us to refer to the URL by its name. The slug of the event 
        # is passed as an argument to generate the correct URL for editing this 
        # specific event. edit_url will be used to access the event edit view.
        self.edit_url = reverse(
            "event_edit",
            args=[self.event.slug]
        )
    
    def test_event_owner_can_access_edit_page(self):
        """
        Test that the event owner can access the event editing page.
        """
        # Arrange: Log in as the event owner as set up in the setUp method. 
        # This user is the creator of the event and should have permission to edit it.
        self.client.login(
            username="eventowner",
            password="testpassword"
        )

        # Act: Request the event editing page
        response = self.client.get(self.edit_url)

        # Assert: The page loads and uses the event form template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_form.html")
    
    def test_edit_form_contains_existing_event(self):
        """
        Test that the edit form is populated with the existing event.
        """
        # Arrange: Log in as the event owner
        self.client.login(
            username="eventowner",
            password="testpassword"
        )

        # Act: Request the event editing page
        response = self.client.get(self.edit_url)

        # Assert: The form is editing the existing event
        self.assertEqual(
            # Check that the form's instance is the same as the event being edited.
            response.context["form"].instance,
            # This checks that the form is pre-filled with the data of the event 
            # being edited, ensuring that the user sees the current details of 
            # the event in the form fields.
            self.event
        )
                
    def test_event_owner_can_update_event(self):
        """
        Test that the event owner can submit valid data
        and update the existing event.
        """
        # Arrange: Log in as the event owner
        self.client.login(
            username="eventowner",
            password="testpassword"
        )

        # Arrange: Prepare updated form data - the post data must include all required fields, 
        # and the date must be in the future to be valid.
        updated_form_data = {
            "title": "Updated Event",
            "description": "This event has been updated.",
            "venue": "Updated Venue",
            "location": "Liverpool",
            "date": "2026-08-20T21:00",
            "genre": "Techno",
            "lineup": "Updated DJ",
        }

        # Act: Submit the updated data
        response = self.client.post(
            self.edit_url,
            data=updated_form_data
        )

        # Assert: Editing did not create a second event
        self.assertEqual(Event.objects.count(), 1)

        # Reload the event with its latest database values. The slug may change when the title changes,
        # so we need to refresh the event instance to get the updated slug and other fields from the database.
        # refresh_from_db() is a method provided by Django's model instances that reloads the instance's data from the database,
        # so that any changes made to the instance in the database are reflected in the instance in memory. This is important
        # after an update operation, as Django still has the old values stored in self.event until we refresh from the database.
        self.event.refresh_from_db()

        # Assert: The original event now contains the updated data
        self.assertEqual(self.event.title, "Updated Event")
        self.assertEqual(
            self.event.description,
            "This event has been updated."
        )
        self.assertEqual(self.event.venue, "Updated Venue")
        self.assertEqual(self.event.location, "Liverpool")
        self.assertEqual(self.event.genre, "Techno")
        self.assertEqual(self.event.lineup, "Updated DJ")

        # Assert: The user is redirected to the event detail page
        self.assertRedirects(
            response,
            reverse(
                "event_detail",
                args=[self.event.slug]
            )
        )
        
    def test_event_owner_can_update_event(self):
        """
        Test that the event owner can update an existing event.
        """
        # Arrange: Log in as the owner
        self.client.login(
            username="eventowner",
            password="testpassword"
        )

        # Arrange: Prepare valid updated form data, including #
        # all required fields and a future date for the event.
        updated_form_data = {
            "title": "Updated Event",
            "description": "This event has been updated.",
            "venue": "Updated Venue",
            "location": "Liverpool",
            "date": "2026-08-20T21:00",
            "genre": "Techno",
            "lineup": "Updated DJ",
        }

        # Act: Submit the updated data to the edit view
        response = self.client.post(
            self.edit_url,
            data=updated_form_data
        )

        # Assert: Check that editing did not create a second event
        self.assertEqual(Event.objects.count(), 1)

        # Reload the event from the database to ensure we have the 
        # latest data after the update.
        self.event.refresh_from_db()

        # Assert: Check that the existing event was updated with the new data from the form submission
        self.assertEqual(self.event.title, "Updated Event")
        # check that the description was updated correctly and message is displayed on the event detail page
        self.assertEqual(
            self.event.description,
            "This event has been updated."
        )
        
        #check that the venue, location, genre, and lineup were updated correctly
        self.assertEqual(self.event.venue, "Updated Venue")
        self.assertEqual(self.event.location, "Liverpool")
        self.assertEqual(self.event.genre, "Techno")
        self.assertEqual(self.event.lineup, "Updated DJ")

        # Assert: The owner is redirected to the event detail page
        self.assertRedirects(
            response,
            reverse(
                "event_detail",
                args=[self.event.slug]
            )
        )
    
    def test_non_owner_cannot_access_edit_page(self):
        """
        Test that a logged-in user cannot edit another user's event.
        """
        # Arrange: Other user created to test that only the event owner can edit the event
        self.client.login(
            username="otheruser",
            password="testpassword"
        )

        # Act: Request the edit page for an event they do not own
        response = self.client.get(self.edit_url)

        # Assert: The user is redirected away from the edit page
        self.assertRedirects(
            response,
            reverse(
                "event_detail",
                args=[self.event.slug]
            )
        )
        
    def test_logged_out_user_is_redirected_from_edit_page(self):
        """
        Test that a logged-out user cannot access the event editing page.
        """
        # Act: Request the edit page without logging in, the user should be redirected to the login page
        response = self.client.get(self.edit_url)

        # Assert: The user is redirected to the login page, with a 302 status code and the correct redirect URL
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            # Use reverse to get the URL for the login page, and append the next parameter to redirect back to 
            # the edit page after login
            f"{reverse('account_login')}?next={self.edit_url}"
        )
        
    def test_invalid_form_does_not_update_event(self):
        """
        Test that invalid form data does not update the existing event.
        """
        # Arrange: Log in as the event owner
        self.client.login(
            username="eventowner",
            password="testpassword"
        )

        invalid_form_data = {
            "title": "",
            "description": "This should not be saved as it's invalid.",
            "venue": "Invalid Venue",
            "location": "Liverpool",
            "date": "2026-08-20T21:00",
            "genre": "Techno",
            "lineup": "Invalid DJ",
        }

        # Act: Submit invalid data - the title is required, so leaving it blank 
        # should trigger a validation error
        response = self.client.post(
            self.edit_url,
            data=invalid_form_data
        )

        # Reload the event from the database
        self.event.refresh_from_db()

        # Assert: The original event was not changed
        self.assertEqual(self.event.title, "Original Event")
        self.assertEqual(self.event.venue, "Original Venue")

        # Assert: The form is redisplayed with an error
        self.assertEqual(response.status_code, 200)
        
        # Assert: The correct template is used for the event edit form
        self.assertTemplateUsed(response, "events/event_form.html")
        
        # Assert: Check that the form contains an error for the title field,
        # showing that it is required
        self.assertFormError(
            response.context["form"],
            "title",
            "This field is required."
        )