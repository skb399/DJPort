from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event, Comment, DJProfile

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
    
    def test_event_list_page_loads(self):
        """
        Test that the event list view returns a 200 status code and uses the correct template
        This test checks that the event list page loads successfully and uses the correct template.
        """    
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    
    def test_event_list_uses_correct_template(self):
        """
        Test that the event list view only displays published events
        and uses the correct template.
        """
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the correct template is used for the event list view
        self.assertTemplateUsed(
            response,
            "events/event_list.html"
        )
    
    
    def test_event_list_only_shows_published_events(self):
        """
        Test that the event list view only shows published events and not draft events
        """
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the published event is in the context and the draft event is not
        self.assertContains(response, "Published Event")
        self.assertNotContains(response, "Draft Event")
        
     
    def test_event_list_shows_message_when_there_are_no_published_events(self):
        """
        Test that the event list view shows a message when there are no published events.
        """
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
    
    
    def test_event_detail_returns_404_for_invalid_slug(self):
        """
        Test that the event detail view returns a 404 response for an invalid slug
        """
        # Act: Make a GET request to the event detail view with a slug that does not exist
        response = self.client.get(
            reverse("event_detail", args=["event-does-not-exist"])
        )

        # Assert: Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)
    
    def test_event_detail_does_not_display_another_event(self):
        """
        Test that the event detail page only displays the requested event and not other incorrect events
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

        # Arrange: Prepare valid updated form data, including
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
        

class EventDeleteViewTests(TestCase):
    """
    Tests for the event_delete view.
    """
    def setUp(self):
        """
        Create an event owner, another user, an event,
        and store the delete URL.
        """
        self.owner = User.objects.create_user(
            username="eventowner",
            password="testpassword"
        )

        # Create another user to test that only the event owner can delete the event
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword"
        )

        # Create an event owned by the event owner user to be used in the delete tests  
        self.event = Event.objects.create(
            creator=self.owner,
            title="Event To Delete",
            slug="event-to-delete",
            description="An event used for deletion tests.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            lineup="Test DJ",
            status=1
        )

        # Store the URL for the event delete page using Django's reverse function.
        # This allows us to refer to the URL by its name instead of hardcoding it.
        self.delete_url = reverse(
            "event_delete",
            args=[self.event.slug]
        )
    
    def test_event_owner_can_access_delete_confirmation_page(self):
        """
        Test that the event owner can access the deletion confirmation page, and that 
        opening the confirmation page does not delete the event. The event should only
        be deleted after the user confirms by submitting the form.
        """
        # Arrange: Log in as the event owner
        self.client.login(
            username="eventowner",
            password="testpassword"
        )

        # Act: Request the delete confirmation page
        response = self.client.get(self.delete_url)

        # Assert: The confirmation page loads correctly, or the user is redirected 
        # to the event detail page if they are not the owner
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "events/event_confirm_delete.html"
        )

        # Assert: A GET request did not delete the event as there is still one event in the database,
        # proving that the event is only deleted after a POST request.
        self.assertEqual(Event.objects.count(), 1)
    
    def test_event_owner_can_delete_event(self):
        """
        Test that the event owner can confirm deletion and remove the event, and that event is actually 
        deleted from the database after the confirmation form is submitted. The event should only be deleted 
        after the user confirms by submitting the form.
        """
        # Arrange: Log in as the event owner
        self.client.login(
            username="eventowner",
            password="testpassword"
        )

        # Act: Submit the deletion confirmation form, which should delete the event and redirect 
        # to the event list page
        response = self.client.post(
            self.delete_url,
            # follow=True tells Django's test client to follow the redirect to the event list, so we
            # can check that the event is no longer displayed on the event list page after deletion.
            follow=True
        )

        # Assert: The event was removed from the database, making the event count zero, proving 
        # that the event is only deleted after a POST request.
        self.assertEqual(Event.objects.count(), 0)

        # Assert: The user was redirected to the event list page after confirming the deletion.
        self.assertRedirects(
            response,
            reverse("event_list")
        )

        # Assert: The deleted event is no longer displayed on the event list page, proving that 
        # the event was successfully deleted and is no longer accessible.
        self.assertNotContains(response, "Event To Delete")
        
    def test_non_owner_cannot_delete_event(self):
        """
        Test that a logged-in user cannot delete another user's event.
        """
        # Arrange: Log in as a different user, to check that only the event owner can delete the event. 
        # The other user should not have permission to delete this event.
        self.client.login(
            username="otheruser",
            password="testpassword"
        )

        # Act: Other usert tries to submit the deletion confirmation form for an event they do not own.
        response = self.client.post(self.delete_url)

        # Assert: The other user is redirected to the event detail page, and the event is not deleted.
        self.assertRedirects(
            response,
            reverse(
                "event_detail",
                args=[self.event.slug]
            )
        )

        # Assert: The event still exists as the count of events in the database is still 1, proving 
        # that the event was not deleted by a non-owner.
        self.assertEqual(Event.objects.count(), 1)
        # Assert: The event still exists in the database, proving that the event was not deleted by a non-owner.
        self.assertTrue(
            # Check that the specific event created in setUp still exists in the database by looking
            # it up using its unique primary key (pk). Rather than only checking the total number of events.
            Event.objects.filter(pk=self.event.pk).exists()
        )
        
    def test_logged_out_user_is_redirected_from_delete_page(self):
        """
        Test that a logged-out user cannot access the event deletion page, even if they type in the delete URL directly. 
        The user should be redirected to the login page, and the event should not be deleted.
        """
        # Act: Request the delete page without logging in
        response = self.client.get(self.delete_url)

        # Assert: The user is redirected to the login page with a 302 status code and the correct redirect URL, 
        # and the event is not deleted.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            # Use reverse to get the URL for the login page, and append the next parameter to redirect back to 
            # the delete page after login. This ensures that the user is asked to log in before they can 
            # access the delete confirmation page.
            f"{reverse('account_login')}?next={self.delete_url}"
        )

        # Assert: The event was not deleted, showing that logged out user cannot cannot delete the event, as it
        # still exists in the database as we look it up using its unique primary key (pk). This proves that the
        # event is only deleted after a POST request by the owner.
        self.assertTrue(
            Event.objects.filter(pk=self.event.pk).exists()
        )
        
    def test_non_owner_cannot_access_delete_confirmation_page(self):
        """
        Test that a logged-in non-owner cannot access another user's
        event deletion confirmation page even if they type in the delete URL directly. 
        The user should be redirected to the event detail page, and the event should not be deleted.
        """
        # Arrange: Log in as a different user
        self.client.login(
            username="otheruser",
            password="testpassword"
        )

        # Act: Attempt to open the delete confirmation page for an event they do not own. 
        # The other user should not have permission to access this page.
        response = self.client.get(self.delete_url)

        # Assert: The user is redirected to the event detail page 
        self.assertRedirects(
            response,
            reverse(
                "event_detail",
                args=[self.event.slug]
            )
        )

        # Assert: The specific event still exists in the database as the count of events in 
        # the database is still 1, and the we can see it's still there by looking up the primary 
        # key, proving that the event was not deleted by a non-owner.
        self.assertEqual(Event.objects.count(), 1)
        self.assertTrue(
            Event.objects.filter(pk=self.event.pk).exists()
        )
        
class CommentViewTests(TestCase):
    """
    Tests for displaying and submitting comments on events.
    """

    def setUp(self):
        """
        Create a user, an event, approved and unapproved comments,
        and store the relevant URLs.
        """
        self.user = User.objects.create_user(
            username="commentuser",
            password="testpassword"
        )

        self.event = Event.objects.create(
            creator=self.user,
            title="Comment Test Event",
            slug="comment-test-event",
            description="An event used for comment tests.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            lineup="Test DJ",
            status=1
        )

        self.approved_comment = Comment.objects.create(
            event=self.event,
            author=self.user,
            body="This comment is approved.",
            approved=True
        )

        self.unapproved_comment = Comment.objects.create(
            event=self.event,
            author=self.user,
            body="This comment is awaiting approval.",
            approved=False
        )

        self.detail_url = reverse(
            "event_detail",
            args=[self.event.slug]
        )

        self.add_comment_url = reverse(
            "add_comment",
            args=[self.event.slug]
        )
    
    def test_approved_comment_is_displayed(self):
        """
        Test that approved comments are displayed on the event detail page.
        """
        # Act - Make a GET request to the event detail view for the event with an approved comment
        response = self.client.get(self.detail_url)

        # Assert: Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert: Check that the response contains the approved comment's body, proving that approved comments are 
        # displayed on the event detail page.
        self.assertContains(
            response,
            "This comment is approved."
        )
        
    def test_unapproved_comment_is_not_displayed(self):
        """
        Test that unapproved comments are hidden from the event detail page.
        """
        # Act - Make a GET request to the event detail view for the event with an unapproved comment
        response = self.client.get(self.detail_url)

        # Assert: Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Assert: Check that the response does not contain the unapproved comment's body, 
        # proving that unapproved comments are not displayed on the event detail page.
        self.assertNotContains(
            response,
            "This comment is awaiting approval."
        )
        
    def test_logged_in_user_can_submit_comment(self):
        """
        Test that a logged-in user can submit a comment on an event.
        """
        # Arrange: Log in as the comment author 
        self.client.login(
            username="commentuser",
            password="testpassword"
        )

        # Act: Submit a valid comment to the add_comment view for the event
        response = self.client.post(
            self.add_comment_url,
            data={
                "body": "This is a new test comment."
            }
        )

        # Assert: A new comment was added to the database, comment count is 3 
        # because we had 2 comments in setUp (1 approved, 1 unapproved) and now 
        # we added a new one.
        self.assertEqual(Comment.objects.count(), 3)

        # Retrieve the newly created comment
        new_comment = Comment.objects.get(
            body="This is a new test comment."
        )

        # Assert: The comment is linked to the correct user and event
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.event, self.event)

        # Assert: New comments require approval by default
        self.assertFalse(new_comment.approved)

        # Assert: The user is redirected back to the event detail page
        self.assertRedirects(
            response,
            self.detail_url
        )
        
    def test_logged_out_user_cannot_submit_comment(self):
        """
        Test that a logged-out user cannot submit a comment.
        """
        # Act: Try to submit a comment without logging in
        response = self.client.post(
            self.add_comment_url,
            data={
                "body": "This comment should not be saved."
            }
        )

        # Assert: The user should be redirected to the login page
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={self.add_comment_url}"
        )

        # Assert: No new comment was created as the user is not logged in, 
        # so the comment count remains 2 (1 approved, 1 unapproved)
        self.assertEqual(Comment.objects.count(), 2)

        # Assert: The comment with the body "This comment should not be saved." 
        # does not exist in the database,
        self.assertFalse(
            Comment.objects.filter(
                body="This comment should not be saved."
            ).exists()
        )
        
    def test_empty_comment_is_not_saved(self):
        """
        Test that an empty comment cannot be submitted.
        """
        # Arrange: Log in as the comment author
        self.client.login(
            username="commentuser",
            password="testpassword"
        )

        # Act: Submit an empty comment body, 
        # which should not be saved to the database
        response = self.client.post(
            self.add_comment_url,
            data={
                "body": ""
            }
        )

        # Assert: No new comment was created, so the comment count 
        # remains 2 (1 approved, 1 unapproved)
        self.assertEqual(Comment.objects.count(), 2)

        # Assert: The user is redirected back to the event detail page
        self.assertRedirects(
            response,
            self.detail_url
        )
        
class FavouriteViewTests(TestCase):
    """
    Tests for adding and removing events from a user's favourites.
    """

    def setUp(self):
        """
        Create a user, an event, and store the relevant URLs.
        """
        
        # Arrange: Create a test user who can log in and favourite events. 
        self.user = User.objects.create_user(
            username="favouriteuser",
            password="testpassword"
        )
        
        # Arrange: Create a test event whose favourited_by field can be 
        # used to track which users have favourited it.
        self.event = Event.objects.create(
            creator=self.user,
            title="Favourite Test Event",
            slug="favourite-test-event",
            description="An event used for favourite tests.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            lineup="Test DJ",
            status=1
        )
        
        # Store the URL for the event detail page and the toggle favourite URL using Django's reverse function.
        # This allows us to refer to the URLs by their names instead of hardcoding them. Allows us to confirm
        # that the user is redirected to the correct page after favouriting or unfavouriting an event.
        self.detail_url = reverse(
            "event_detail",
            args=[self.event.slug]
        )

        # Store the URL for toggling the favourite status of the event. This URL will be used to test adding 
        # and removing the event from the user's favourites.
        self.favourite_url = reverse(
            "toggle_favourite",
            args=[self.event.slug]
        )
    def test_logged_in_user_can_favourite_an_event(self):
        """
        Test that a logged-in user can add an event to their favourites.
        """
        # Arrange: Log in as the test user
        self.client.login(
            username="favouriteuser",
            password="testpassword"
        )

        # Act: Send a POST request to toggle the favourite status of the event
        response = self.client.post(self.favourite_url)
    
        # Act: Reload the event from the database to ensure the favourite
        # relationship reflects the latest changes after the POST request
        self.event.refresh_from_db()

        # Assert: The user is redirected back to the event detail page
        self.assertRedirects(response, self.detail_url)

        # Assert: The event is now in the user's favourites, proving that the manyto-many 
        # relationship between the user and the event was successfully created.
        self.assertTrue(self.event.favourited_by.filter(id=self.user.id).exists())
        
    def test_logged_in_user_can_remove_event_from_favourites(self):
        """
        Test that a logged-in user can remove an event from their favourites.
        """

        # Arrange: Log in as the test user
        self.client.login(
            username="favouriteuser",
            password="testpassword"
        )

        # Arrange: Add the event to the user's favourites before testing removal
        self.event.favourited_by.add(self.user)

        # Act: Send a POST request to toggle the favourite status of the event
        response = self.client.post(self.favourite_url)

        # Reload the event from the database to ensure the favourite
        # relationship reflects the latest changes after the POST request.
        self.event.refresh_from_db()

        # Assert: The user is redirected back to the event detail page
        self.assertRedirects(response, self.detail_url)

        # Assert: The event is no longer in the user's favourites
        self.assertFalse(
            self.event.favourited_by.filter(id=self.user.id).exists()
        )
        
    def test_logged_out_user_cannot_favourite_an_event(self):
        """
        Test that a logged-out user cannot add an event to their favourites.
        """

        # Act: Try to favourite the event without logging in
        response = self.client.post(self.favourite_url)

        # Reload the event from the database to ensure the favourite
        # relationship reflects the latest changes after the POST request.
        self.event.refresh_from_db()

        # Assert: The user is redirected to the login page because
        # the view is protected by the @login_required decorator.
        self.assertRedirects(
            response,
            f"/accounts/login/?next={self.favourite_url}"
        )

        # Assert: The event has not been added to the user's favourites.
        self.assertFalse(
            self.event.favourited_by.filter(id=self.user.id).exists()
    )
    
    def test_favourites_are_specific_to_each_user(self):
        """
        Test that favouriting an event only applies to the logged-in user.
        """
        
        # Arrange: Create a second user so we can verify that favourites
        # are stored separately for each user.
        other_user = User.objects.create_user(
            username="otherfavouriteuser",
            password="testpassword"
        )

        # Add the event to the original user's favourites, so we can 
        # check that the other user does not have it in their favourites.
        self.event.favourited_by.add(self.user)

        # Assert: The original user has favourited the event, showing that 
        # the many-to-many relationship is working correctly for that user.
        self.assertTrue(
            self.event.favourited_by.filter(id=self.user.id).exists()
        )

        # Assert: The second user has not favourited the event, proving that 
        # favouriting is specific to each user and does not affect other users' favourites.
        self.assertFalse(
            self.event.favourited_by.filter(id=other_user.id).exists()
        )
    
    def test_event_detail_shows_correct_favourite_status(self):
        """
        Test that the event detail view correctly identifies
        whether the logged-in user has favourited the event.
        """
        # Arrange: Log in and favourite the event, so we can check that the event detail view 
        # correctly identifies the favourite status for the logged-in user.
        self.client.login(
            username="favouriteuser",
            password="testpassword"
        )
        
        # Arrange: Add the event to the user's favourites so the
        # event detail view should recognise it as favourited.
        self.event.favourited_by.add(self.user)

        # Act: Request the event detail page for the event
        response = self.client.get(self.detail_url)

        # Assert: The view passes True for is_favourited in the context, showing that the logged-in 
        # user has favourited the event.
        self.assertTrue(response.context["is_favourited"])
        
    def test_event_detail_shows_unfavourited_status(self):
        """
        Test that the event detail view correctly identifies
        when the logged-in user has not favourited the event.
        """

        # Arrange: Log in as the test user without favouriting the event,
        # so we can check that the event detail view correctly identifies
        # that the event has not been favourited.
        self.client.login(
            username="favouriteuser",
            password="testpassword"
        )

        # Act: Request the event detail page for the event, which should
        # include the favourite status in the context.
        response = self.client.get(self.detail_url)

        # Assert: The view passes False for is_favourited in the context,
        # indicating that the logged-in user has not favourited the event.
        self.assertFalse(response.context["is_favourited"])
        
class DJProfileCreateViewTests(TestCase):
    """
    Tests for creating DJ profiles.
    """

    def setUp(self):
        """
        Create a test user and store the DJ profile creation URL.
        """
        self.user = User.objects.create_user(
            username="djuser",
            password="testpassword"
        )

        # Store the URL for creating a DJ profile using Django's reverse function. 
        # This allows us to refer to the URL by its name instead of hardcoding it. 
        self.create_url = reverse("dj_profile_create")
        
    def test_logged_in_user_can_access_dj_profile_create_page(self):
        """
        Test that a logged-in user can access the DJ Profile creation page.
        """
        # Arrange: Log the test user in
        self.client.login(
            username="djuser",
            password="testpassword"
        )

        # Act: Request the dj profile creation page, which should be accessible to logged-in users
        response = self.client.get(self.create_url)

        # Assert: The page loads and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_form.html")
        
    def test_logged_out_user_cannot_access_dj_profile_create_page(self):
        """
        Test that a logged-out user cannot access the dj profile creation page.
        """
        # Act: Request the protected page without logging in, the user should be redirected to the login page
        response = self.client.get(self.create_url)

        # Assert: The user is redirected to the login page, with a 302 status code and the correct redirect URL
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={self.create_url}"
        )
        
    def test_logged_in_user_can_create_dj_profile(self):
        """
        Test that a logged-in user can submit valid data
        and create a new DJ profile.
        """
        # Arrange: Log the user in
        self.client.login(
            username="djuser",
            password="testpassword"
        )

        # Arrange: Prepare valid form data for creating a new DJ profile. image, website, and social_media fields 
        # not included because they're optional
        form_data = {
            "dj_name": "Test DJ",
            "bio": "A test DJ profile created through the form.",
            "genres": "Test genre",
            "location": "Manchester",
        }

        # Act: Submit the form, which should create a new DJ profile.
        response = self.client.post(
            self.create_url,
            data=form_data
        )

        # Assert: One DJ profile was created.
        self.assertEqual(DJProfile.objects.count(), 1)

        # Retrieve the created DJ profile so we can inspect it.
        dj_profile = DJProfile.objects.get()

        # Assert: The view assigned the logged-in user as owner.
        self.assertEqual(dj_profile.owner, self.user)

        # Assert: The submitted DJ name was saved correctly.
        self.assertEqual(dj_profile.dj_name, "Test DJ")

        # Assert: The user is redirected to the homepage after creation.
        self.assertRedirects(response, reverse("home"))
        
    def test_user_cannot_create_second_dj_profile(self):
        """
        Test that a user cannot create more than one DJ profile.
        """
        # Arrange: Log the user in
        self.client.login(
            username="djuser",
            password="testpassword"
        )

        # Arrange: Create an initial DJ profile for the user, so we 
        # can test that they cannot create a second one.
        DJProfile.objects.create(
            owner=self.user,
            dj_name="Existing DJ",
            bio="An existing DJ profile.",
            genres="Existing genre",
            location="Manchester"
        )

        # Act: Attempt to create a second DJ profile for the same user
        response = self.client.post(
            self.create_url,
            data={
                "dj_name": "Second DJ",
                "bio": "Attempting to create a second DJ profile.",
                "genres": "Second genre",
                "location": "Liverpool"
            }
        )

        # Assert: The user is redirected to the homepage.
        self.assertRedirects(response, reverse("home"))

        # Assert: No second DJ profile was created.
        self.assertEqual(DJProfile.objects.count(), 1)

        # Assert: A warning message tells the user that they already have a DJ profile.
        messages_list = list(response.wsgi_request._messages)

        self.assertEqual(
            str(messages_list[0]),
            "You already have a DJ profile."
        )
        
    def test_invalid_form_does_not_create_dj_profile(self):
        """
        Test that invalid DJ profile form data does not create a profile.
        """
        # Arrange: Log the user in
        self.client.login(
            username="djuser",
            password="testpassword"
        )

        # Arrange: Prepare invalid form data with the required DJ name missing. 
        # " " used for dj_name to simulate a user submitting a form without 
        # filling in the required field.
        invalid_form_data = {
            "dj_name": "",
            "bio": "A DJ profile without a name.",
            "genres": "House",
            "location": "Manchester",
        }

        # Act: Submit the invalid form data.
        response = self.client.post(
            self.create_url,
            data=invalid_form_data
        )

        # Assert: No DJ profile was created, as the profile count remains 0, proving
        # that invalid form data does not create a new DJ profile.
        self.assertEqual(DJProfile.objects.count(), 0)

        # Assert: The form is redisplayed instead of redirecting.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "events/dj_profile_form.html"
        )

        # Assert: The DJ name field contains the expected validation error.
        self.assertFormError(
            response.context["form"],
            "dj_name",
            "This field is required."
        )
        
class DJProfileViewTests(TestCase):
    """
    Tests for viewing DJ profiles. 
    """

    def setUp(self):
        """
        Create a user, a DJ profile, and store the relevant URLs.
        """
        
        # Arrange: Create a test user who can log in and view DJ profiles.
        self.user = User.objects.create_user(
            username="djviewer",
            password="testpassword"
        )

        # Arrange: Create a DJ profile for the test user, which will be used to test viewing DJ profiles.
        self.dj_profile = DJProfile.objects.create(
            owner=self.user,
            dj_name="Test DJ",
            slug="test-dj",
            bio="A DJ profile used for view tests.",
            genres="House, Techno",
            location="Manchester",
            website="https://example.com",
            social_media="https://instagram.com/testdj"
        )

        # Store the URL for the DJ profile list and detail pages using Django's reverse function.
        # This allows us to refer to the URLs by their names instead of hardcoding them.
        self.list_url = reverse("dj_profile_list")

        # Store the URL for the DJ profile detail page using the slug of the created DJ profile.
        self.detail_url = reverse(
            "dj_profile_detail",
            args=[self.dj_profile.slug]
        )
        
    def test_dj_profile_list_page_loads_successfully(self):
        """
        Test that the DJ profile list page loads successfully and uses the correct template.
        """
        # Act: Request the DJ profile list page
        response = self.client.get(self.list_url)

        # Assert: The page loads with a 200 status code and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_list.html")
        
    def test_dj_profile_list_displays_dj_profile(self):
        """
        Test that a DJ profile is displayed on the DJ profile list page.
        """ 
        # Act: Request the DJ profile list page
        response = self.client.get(self.list_url)

        # Assert: The page contains the DJ name of the created DJ profile, proving that it is displayed on the list page.
        self.assertContains(response, "Test DJ")
        
    def test_dj_profile_detail_page_loads_successfully(self):
        """
        Test that a DJ profile detail page loads successfully
        and uses the correct template.
        """
        # Act: Request the DJ profile detail page for the created DJ profile
        response = self.client.get(self.detail_url)

        # Assert: The page loads with a 200 status code and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_detail.html")
        
    def test_dj_profile_detail_displays_correct_profile(self):
        """
        Test that the DJ profile detail page displays
        the correct DJ profile information.
        """
        # Act: Request the DJ profile detail page for the created DJ profile
        response = self.client.get(self.detail_url)

        # Assert: The page contains the DJ name, bio, genres, location, website, and social media of the created DJ profile,
        # proving that the correct profile information is displayed on the detail page.
        self.assertContains(response, "Test DJ")
        self.assertContains(response, "A DJ profile used for view tests.")
        self.assertContains(response, "House, Techno")
        self.assertContains(response, "Manchester")
        self.assertContains(response, "https://example.com")
        self.assertContains(response, "https://instagram.com/testdj")
        
    def test_invalid_dj_profile_slug_returns_404(self):
        """
        Test that requesting a DJ profile that does not exist
        returns a 404 response.
        """
        # Act: Request a DJ profile detail page with an invalid slug
        response = self.client.get(reverse("dj_profile_detail", args=["nonexistent-dj"]))

        # Assert: The response status code is 404, showing that the requested DJ profile does not exist.
        self.assertEqual(response.status_code, 404)