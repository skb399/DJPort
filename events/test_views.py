from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Event, Comment, DJProfile


class EventListViewTests(TestCase):
    # Arrange: Set up test data for the EventListView tests
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a published event and a draft event for testing
        self.published_event = Event.objects.create(
            creator=self.user,
            title="Published Event",
            slug="published-event",
            description="A published event.",
            venue="Test Venue",
            lineup="DJ Test",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            status=1,
        )

        # Create a draft event to test that it does not appear
        # in the event list view
        self.draft_event = Event.objects.create(
            creator=self.user,
            title="Draft Event",
            slug="draft-event",
            description="A draft event.",
            venue="Private Venue",
            location="Bristol",
            date=timezone.now(),
            genre="Techno",
            status=0,
        )

    def test_event_list_page_loads(self):
        """
        Test that the event list view returns a 200 status
        code and uses the correct template. This test checks
        that the event list page loads successfully and uses
        the correct template.
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
        # Assert: Check that the correct template is used for the
        # event list view
        self.assertTemplateUsed(response, "events/event_list.html")

    def test_event_list_only_shows_published_events(self):
        """
        Test that the event list view only shows published events
        and not draft events
        """
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the published event is in the context
        # and the draft event is not
        self.assertContains(response, "Published Event")
        self.assertNotContains(response, "Draft Event")

    def test_event_list_shows_message_when_there_are_no_published_events(self):
        """
        Test that the event list view shows a message when there are no 
        published events.
        """
        # Delete the published event to simulate no published events
        self.published_event.delete()
        # Act: Make a GET request to the event list view
        response = self.client.get(reverse("event_list"))
        # Assert: Check that the response contains the message indicating no 
        # published events are available
        self.assertContains(response,
            "No published events are currently available."
        )
        self.assertNotContains(response, "Draft Event")

    # -------------------------------------------------
    # Event Search Tests
    # --------------------------------------------------
    def test_search_finds_event_by_title(self):
        """
        Test that searching by event title returns the matching published 
        event.
        """
        # Act: Make a GET request to the event list view with a search query
        # for the published event's title
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass
            # the search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # the value being the title of the published event.
            {"q": "Published"},
        )
        # Assert: Check that the response contains the published event's title,
        # indicating that the search was successful
        self.assertContains(response, "Published Event")

    def test_search_finds_event_by_venue(self):
        """
        Test that searching by venue returns the matching published event.
        """
        # Act: Make a GET request to the event list view with a search query
        # for the published event's venue
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass
            # the search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # the value being the venue of the published event.
            {"q": "Test Venue"},
        )
        # Assert: Check that the response contains the published event's title,
        # indicating that the search was successful
        self.assertContains(response, "Published Event")

    def test_search_finds_event_by_location(self):
        """
        Test that searching by location returns the matching published event.
        """
        # Act: Make a GET request to the event list view with a search query
        # for the published event's location
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass
            # the search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # the value being the location of the published event.
            {"q": "Manchester"},
        )
        # Assert: Check that the response contains the published event's title,
        # indicating that the search was successful
        self.assertContains(response, "Published Event")

    def test_search_finds_event_by_genre(self):
        """
        Test that searching by genre returns the matching published event.
        """
        # Act: Make a GET request to the event list view with a search query
        # for the published event's genre
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass the
            # search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # the value being the genre of the published event.
            {"q": "House"},
        )
        # Assert: Check that the response contains the published event's title,
        # indicating that the search was successful
        self.assertContains(response, "Published Event")

    def test_search_finds_event_by_lineup(self):
        """
        Test that searching by an artist in the lineup returns
        the matching published event.
        """
        # Act: Search for an artist listed in the event lineup.
        response = self.client.get(reverse("event_list"), {"q": "DJ Test"})

        # Assert: The matching published event is displayed.
        self.assertContains(response, "Published Event")

    def test_search_is_case_insensitive(self):
        """
        Test that event search is case-insensitive.
        """
        # Act: Make a GET request to the event list view with a search query in
        # a different case than the published event's title
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass the
            # search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # the value being the title of the published event in a different
            # case.
            {"q": "manchester"},
        )
        # Assert: Check that the response contains the published event's title,
        # indicating that the search was successful and case-insensitive
        self.assertContains(response, "Published Event")

    def test_search_shows_message_when_no_events_match(self):
        """
        Test that a message is displayed when no published events
        match the search query.
        """
        # Act: Make a GET request to the event list view with a search query
        # that does not match any published events
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass
            # the search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # the value is a string that does not match any published events.
            {"q": "NoSuchEvent"},
        )
        # Assert: Check that the response contains the message indicating no
        # events were found matching the search query
        self.assertContains(
            response,
            'No events found matching "NoSuchEvent".'
            )

    def test_empty_search_shows_normal_event_list(self):
        """
        Test that an empty search displays the normal published event list.
        """
        # Act: Make a GET request to the event list view with an empty search
        # query
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass an
            # empty search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # an empty string as the value, simulating an empty search.
            {"q": ""},
        )
        # Assert: Check that the response contains the published event's title
        # and does not contain the draft event's title,
        # showing that the normal event list is displayed
        self.assertContains(response, "Published Event")
        self.assertNotContains(response, "Draft Event")

    def test_search_does_not_show_matching_draft_events(self):
        """
        Test that search results only contain published events,
        even when a draft event matches the search query.
        """
        # Act: Make a GET request to the event list view with a search query
        # that matches the draft event's location
        response = self.client.get(
            # Use reverse to get the URL for the event list view, and pass the
            # search query as a GET parameter
            reverse("event_list"),
            # The search query is passed as a dictionary with the key "q" and
            # the value being the location of the draft event.
            {"q": "Bristol"},
        )
        # Assert: Check that the response does not contain the draft event's
        # title, indicating that draft events are not
        # shown in search results
        self.assertNotContains(response, "Draft Event")


class EventDetailViewTests(TestCase):
    # Arrange: Set up test data for the EventDetailView tests
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
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
            status=1,
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
        # Act: Make a GET request to the event detail view for the published
        # event
        response = self.client.get(
            reverse("event_detail", args=[self.published_event.slug])
        )

        # Assert: Check that the response status code is 200 (OK) and the
        # correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_detail.html")

    def test_event_detail_displays_correct_event_information(self):
        """
        Test that the event detail page displays the correct event information.
        """
        # Act: Make a GET request to the event detail view for the published
        # event
        response = self.client.get(
            reverse("event_detail", args=[self.published_event.slug])
        )
        # Assert: Check that the response contains the event's title, venue,
        # location, description, and genre
        self.assertContains(response, self.published_event.title)
        self.assertContains(response, self.published_event.venue)
        self.assertContains(response, self.published_event.location)
        self.assertContains(response, self.published_event.description)
        self.assertContains(response, self.published_event.genre)

    def test_event_detail_returns_404_for_invalid_slug(self):
        """
        Test that the event detail view returns a 404 response for an invalid slug
        """
        # Act: Make a GET request to the event detail view with a slug that
        # does not exist
        response = self.client.get(
            reverse("event_detail", args=["event-does-not-exist"])
        )

        # Assert: Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

    def test_event_detail_does_not_display_another_event(self):
        """
        Test that the event detail page only displays the requested event and
        not other incorrect events
        """
        # Act: Make a GET request to the event detail view for the published
        # event
        response = self.client.get(
            reverse("event_detail", args=[self.published_event.slug])
        )
        # Assert: Check that the response does not contain information from
        # the other event
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
            username="testuser", password="testpassword"
        )
        # Store the URL for the event creation page using Django's reverse
        # function
        # which allows us to refer to the URL by its name instead of
        # hardcoding it.
        self.create_url = reverse("event_create")

    def test_logged_in_user_can_access_event_create_page(self):
        """
        Test that a logged-in user can access the event creation page.
        """
        # Arrange: Log the test user in
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the event creation page, which should be accessible to
        # logged-in users
        response = self.client.get(self.create_url)

        # Assert: The page loads and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_form.html")

    def test_logged_out_user_is_redirected_from_event_create_page(self):
        """
        Test that a logged-out user cannot access the event creation page.
        """
        # Act: Request the protected page without logging in, the user should
        # be redirected to the login page
        response = self.client.get(self.create_url)

        # Assert: The user is redirected to the login page, with a 302 status
        # code and the correct redirect URL
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.create_url}"
        )

    def test_logged_in_user_can_create_event(self):
        """
        Test that a logged-in user can submit valid data
        and create a new event.
        """
        # Arrange: Log the user in
        self.client.login(username="testuser", password="testpassword")

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
        response = self.client.post(self.create_url, data=form_data)

        # Assert: One event was created, and the event's details match the
        # submitted data
        self.assertEqual(Event.objects.count(), 1)

        # Retrieve the created event so we can inspect it. There are no events
        # created in this tests'
        # setUp, so after the post there should be exactly one event in the
        # database, which we can retrieve with get().
        created_event = Event.objects.get()

        # Assert: The view assigned the logged-in user as creator
        self.assertEqual(created_event.creator, self.user)

        # Assert: The submitted title was saved, and the event's title matches
        # the form data
        self.assertEqual(created_event.title, "Test Club Night")

        # Assert: The user was redirected to the new event detail page
        self.assertRedirects(
            response,
            # Use reverse to get the URL for the event detail page, passing
            # the slug of the created event as an argument
            reverse(
                "event_detail",
                # Use the slug of the created event to generate the correct
                # URL for the detail view
                args=[created_event.slug],
            ),
        )

    def test_invalid_form_does_not_create_event(self):
        """
        Test that invalid form data does not create an event
        and redisplays the event form.
        """
        # Arrange: Log the user in
        self.client.login(username="testuser", password="testpassword")

        # Arrange: Submit form data without the required title
        invalid_form_data = {
            # Title is required, so leaving it blank should trigger a
            # validation error
            "title": "",
            "description": "An event without a title.",
            "venue": "Test Venue",
            "location": "Manchester",
            "date": "2026-08-15T22:00",
            "genre": "House",
            "lineup": "DJ Test",
        }

        # Act: Submit the invalid form
        response = self.client.post(self.create_url, data=invalid_form_data)

        # Assert: No event was saved, this proves that the invalid submission
        # did not create affect the database, and the event count remains zero
        self.assertEqual(Event.objects.count(), 0)

        # Assert: This proves that the user stays on the event creation page
        # and sees the form again, with validation errors displayed, instead
        # of being redirected to another page. The response status code is 200,
        # indicating that the form was redisplayed, and the correct template 
        # is used.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_form.html")

        self.assertFormError(
            response.context["form"], "title", "This field is required."
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
            username="eventowner", password="testpassword"
        )
        # other user created to test that only the event owner can edit the
        # event
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )
        # Create an event owned by the event owner user to be used in the edit
        # tests
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
            status=1,
        )
        # Store the URL for the event edit page using Django's reverse 
        # function. This allows us to refer to the URL by its name. The slug of
        # the event passed as an argument to generate the correct URL for 
        # editing this specific event. edit_url will be used to access the
        # event edit view.
        self.edit_url = reverse("event_edit", args=[self.event.slug])

    def test_event_owner_can_access_edit_page(self):
        """
        Test that the event owner can access the event editing page.
        """
        # Arrange: Log in as the event owner as set up in the setUp method.
        # This user is the creator of the event and should have permission to
        # edit it.
        self.client.login(username="eventowner", password="testpassword")

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
        self.client.login(username="eventowner", password="testpassword")

        # Act: Request the event editing page
        response = self.client.get(self.edit_url)

        # Assert: The form is editing the existing event
        self.assertEqual(
            # Check that the form's instance is the same as the event being
            # edited.
            response.context["form"].instance,
            # This checks that the form is pre-filled with the data of the
            # event being edited, ensuring that the user sees the current 
            # details of the event in the form fields.
            self.event,
        )

    def test_event_owner_can_update_event(self):
        """
        Test that the event owner can submit valid data
        and update the existing event.
        """
        # Arrange: Log in as the event owner
        self.client.login(username="eventowner", password="testpassword")

        # Arrange: Prepare updated form data - the post data must include all
        # required fields, and the date must be in the future to be valid.
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
        response = self.client.post(self.edit_url, data=updated_form_data)

        # Assert: Editing did not create a second event
        self.assertEqual(Event.objects.count(), 1)

        # Reload the event with its latest database values. The slug may
        # change when the title changes, so we need to refresh the event
        # instance to get the updated slug and other fields from the database.
        # refresh_from_db() is a method provided by Django's model instances
        # that reloads the instance's data from the database, so that any 
        # changes made to the instance in the database are reflected in the 
        # instance in memory. This is important after an update operation, as
        # Django still has the old values stored in self.event until we 
        # refresh from the database.
        self.event.refresh_from_db()

        # Assert: The original event now contains the updated data
        self.assertEqual(self.event.title, "Updated Event")
        self.assertEqual(
            self.event.description,
            "This event has been updated.")
        self.assertEqual(self.event.venue, "Updated Venue")
        self.assertEqual(self.event.location, "Liverpool")
        self.assertEqual(self.event.genre, "Techno")
        self.assertEqual(self.event.lineup, "Updated DJ")

        # Assert: The user is redirected to the event detail page
        self.assertRedirects(response, reverse("event_detail", args=[self.event.slug]))

    def test_event_owner_can_update_event(self):
        """
        Test that the event owner can update an existing event.
        """
        # Arrange: Log in as the owner
        self.client.login(username="eventowner", password="testpassword")

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
        response = self.client.post(self.edit_url, data=updated_form_data)

        # Assert: Check that editing did not create a second event
        self.assertEqual(Event.objects.count(), 1)

        # Reload the event from the database to ensure we have the
        # latest data after the update.
        self.event.refresh_from_db()

        # Assert: Check that the existing event was updated with the new data
        # from the form submission
        self.assertEqual(self.event.title, "Updated Event")
        # check that the description was updated correctly and message is 
        # displayed on the event detail page
        self.assertEqual(
            self.event.description,
            "This event has been updated."
            )

        # check that the venue, location, genre, and lineup were updated
        # correctly
        self.assertEqual(self.event.venue, "Updated Venue")
        self.assertEqual(self.event.location, "Liverpool")
        self.assertEqual(self.event.genre, "Techno")
        self.assertEqual(self.event.lineup, "Updated DJ")

        # Assert: The owner is redirected to the event detail page
        self.assertRedirects(response, reverse("event_detail", args=[self.event.slug]))

    def test_non_owner_cannot_access_edit_page(self):
        """
        Test that a logged-in user cannot edit another user's event.
        """
        # Arrange: Other user created to test that only the event owner
        # can edit the event
        self.client.login(username="otheruser", password="testpassword")

        # Act: Request the edit page for an event they do not own
        response = self.client.get(self.edit_url)

        # Assert: The user is redirected away from the edit page
        self.assertRedirects(response, reverse("event_detail", args=[self.event.slug]))

    def test_logged_out_user_is_redirected_from_edit_page(self):
        """
        Test that a logged-out user cannot access the event editing page.
        """
        # Act: Request the edit page without logging in, the user should be
        # redirected to the login page
        response = self.client.get(self.edit_url)

        # Assert: The user is redirected to the login page, with a 302 status
        # code and the correct redirect URL
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            # Use reverse to get the URL for the login page, and append the
            # next parameter to redirect back to the edit page after login
            f"{reverse('account_login')}?next={self.edit_url}",
        )

    def test_invalid_form_does_not_update_event(self):
        """
        Test that invalid form data does not update the existing event.
        """
        # Arrange: Log in as the event owner
        self.client.login(username="eventowner", password="testpassword")

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
        response = self.client.post(self.edit_url, data=invalid_form_data)

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
            response.context["form"], "title", "This field is required."
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
            username="eventowner", password="testpassword"
        )

        # Create another user to test that only the event owner can delete the
        # event
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )

        # Create an event owned by the event owner user to be used in the
        # delete tests
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
            status=1,
        )

        # Store the URL for the event delete page using Django's reverse 
        # function. This allows us to refer to the URL by its name instead
        # of hardcoding it.
        self.delete_url = reverse("event_delete", args=[self.event.slug])

    def test_event_owner_can_access_delete_confirmation_page(self):
        """
        Test that the event owner can access the deletion confirmation page,
        and that opening the confirmation page does not delete the event. The
        event should only be deleted after the user confirms by submitting the
        form.
        """
        # Arrange: Log in as the event owner
        self.client.login(username="eventowner", password="testpassword")

        # Act: Request the delete confirmation page
        response = self.client.get(self.delete_url)

        # Assert: The confirmation page loads correctly, or the user is 
        # redirected to the event detail page if they are not the owner
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_confirm_delete.html")

        # Assert: A GET request did not delete the event as there is still one
        # event in the database, proving that the event is only deleted after
        # a POST request.
        self.assertEqual(Event.objects.count(), 1)

    def test_event_owner_can_delete_event(self):
        """
        Test that the event owner can confirm deletion and remove the event,
        and that event is actually deleted from the database after the
        confirmation form is submitted. The event should only be deleted
        after the user confirms by submitting the form.
        """
        # Arrange: Log in as the event owner
        self.client.login(username="eventowner", password="testpassword")

        # Act: Submit the deletion confirmation form, which should delete the
        # event and redirect
        # to the event list page
        response = self.client.post(
            self.delete_url,
            # follow=True tells Django's test client to follow the redirect to
            # the event list, so we can check that the event is no longer
            # displayed on the event list page after deletion.
            follow=True,
        )

        # Assert: The event was removed from the database, making the event
        # count zero, proving that the event is only deleted after a POST 
        # request.
        self.assertEqual(Event.objects.count(), 0)

        # Assert: The user was redirected to the event list page after
        # confirming the deletion.
        self.assertRedirects(response, reverse("event_list"))

        # Assert: The deleted event is no longer displayed on the event
        # list page, proving that the event was successfully deleted and is
        # no longer accessible.
        self.assertNotContains(response, "Event To Delete")

    def test_non_owner_cannot_delete_event(self):
        """
        Test that a logged-in user cannot delete another user's event.
        """
        # Arrange: Log in as a different user, to check that only the event
        # owner can delete the event. The other user should not have 
        # permission to delete this event.
        self.client.login(username="otheruser", password="testpassword")

        # Act: Other usert tries to submit the deletion confirmation form for
        # an event they do not own.
        response = self.client.post(self.delete_url)

        # Assert: The other user is redirected to the event detail page, and
        # the event is not deleted.
        self.assertRedirects(response, reverse("event_detail", args=[self.event.slug]))

        # Assert: The event still exists as the count of events in the
        # database is still 1, proving that the event was not deleted by a
        # non-owner.
        self.assertEqual(Event.objects.count(), 1)
        # Assert: The event still exists in the database, proving that the
        # event was not deleted by a non-owner.
        self.assertTrue(
            # Check that the specific event created in setUp still exists in
            # the database by looking it up using its unique primary key (pk).
            # Rather than only checking the total number of events.
            Event.objects.filter(pk=self.event.pk).exists()
        )

    def test_logged_out_user_is_redirected_from_delete_page(self):
        """
        Test that a logged-out user cannot access the event deletion page,
        even if they type in the delete URL directly. The user should be
        redirected to the login page, and the event should not be deleted.
        """
        # Act: Request the delete page without logging in
        response = self.client.get(self.delete_url)

        # Assert: The user is redirected to the login page with a 302 status
        # code and the correct redirect URL, and the event is not deleted.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            # Use reverse to get the URL for the login page, and append the
            # next parameter to redirect back to the delete page after login.
            # This ensures that the user is asked to log in before they can
            # access the delete confirmation page.
            f"{reverse('account_login')}?next={self.delete_url}",
        )

        # Assert: The event was not deleted, showing that logged out user
        # cannot cannot delete the event, as it still exists in the database
        # as we look it up using its unique primary key (pk). This proves
        # that the event is only deleted after a POST request by the owner.
        self.assertTrue(Event.objects.filter(pk=self.event.pk).exists())

    def test_non_owner_cannot_access_delete_confirmation_page(self):
        """
        Test that a logged-in non-owner cannot access another user's
        event deletion confirmation page even if they type in the delete URL
        directly. The user should be redirected to the event detail page, and
        the event should not be deleted.
        """
        # Arrange: Log in as a different user
        self.client.login(username="otheruser", password="testpassword")

        # Act: Attempt to open the delete confirmation page for an event they
        # do not own. The other user should not have permission to access this
        # page.
        response = self.client.get(self.delete_url)

        # Assert: The user is redirected to the event detail page
        self.assertRedirects(response,
                             reverse(
                                 "event_detail",
                                 args=[self.event.slug]
                                 )
                             )

        # Assert: The specific event still exists in the database as the count
        # of events in the database is still 1, and the we can see it's still
        # there by looking up the primary key, proving that the event was not
        # deleted by a non-owner.
        self.assertEqual(Event.objects.count(), 1)
        self.assertTrue(Event.objects.filter(pk=self.event.pk).exists())


# ------------------------------------------------------------
# COMMENT VIEW TESTS
# -----------------------------------------------------------


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
            username="commentuser", password="testpassword"
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
            status=1,
        )

        self.approved_comment = Comment.objects.create(
            event=self.event,
            author=self.user,
            body="This comment is approved.",
            approved=True,
        )

        self.unapproved_comment = Comment.objects.create(
            event=self.event,
            author=self.user,
            body="This comment is awaiting approval.",
            approved=False,
        )

        self.detail_url = reverse("event_detail", args=[self.event.slug])

        self.add_comment_url = reverse("add_comment", args=[self.event.slug])

    def test_approved_comment_is_displayed(self):
        """
        Test that approved comments are displayed on the event detail page.
        """
        # Act - Make a GET request to the event detail view for the event with
        # an approved comment
        response = self.client.get(self.detail_url)

        # Assert: Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert: Check that the response contains the approved comment's body,
        # proving that approved comments are
        # displayed on the event detail page.
        self.assertContains(response, "This comment is approved.")

    def test_unapproved_comment_is_not_displayed(self):
        """
        Test that unapproved comments are hidden from the event detail page.
        """
        # Act - Make a GET request to the event detail view for the event with
        # an unapproved comment
        response = self.client.get(self.detail_url)

        # Assert: Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert: Check that the response does not contain the unapproved
        # comment's body, proving that unapproved comments are not displayed
        # on the event detail page.
        self.assertNotContains(response, "This comment is awaiting approval.")

    def test_logged_in_user_can_submit_comment(self):
        """
        Test that a logged-in user can submit a comment on an event.
        """
        # Arrange: Log in as the comment author
        self.client.login(username="commentuser", password="testpassword")

        # Act: Submit a valid comment to the add_comment view for the event
        response = self.client.post(
            self.add_comment_url, data={"body": "This is a new test comment."}
        )

        # Assert: A new comment was added to the database, comment count is 3
        # because we had 2 comments in setUp (1 approved, 1 unapproved) and
        # now we added a new one.
        self.assertEqual(Comment.objects.count(), 3)

        # Retrieve the newly created comment
        new_comment = Comment.objects.get(body="This is a new test comment.")

        # Assert: The comment is linked to the correct user and event
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.event, self.event)

        # Assert: New comments require approval by default
        self.assertFalse(new_comment.approved)

        # Assert: The user is redirected back to the event detail page
        self.assertRedirects(response, self.detail_url)

    def test_logged_out_user_cannot_submit_comment(self):
        """
        Test that a logged-out user cannot submit a comment.
        """
        # Act: Try to submit a comment without logging in
        response = self.client.post(
            self.add_comment_url, data={"body": "This comment should not be "
                                        "saved."}
        )

        # Assert: The user should be redirected to the login page
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.add_comment_url}"
        )

        # Assert: No new comment was created as the user is not logged in,
        # so the comment count remains 2 (1 approved, 1 unapproved)
        self.assertEqual(Comment.objects.count(), 2)

        # Assert: The comment with the body "This comment should not be saved."
        # does not exist in the database,
        self.assertFalse(
            Comment.objects.filter(body="This comment should not be "
                                       "saved.").exists()
        )

    def test_empty_comment_is_not_saved(self):
        """
        Test that an empty comment cannot be submitted.
        """
        # Arrange: Log in as the comment author
        self.client.login(username="commentuser", password="testpassword")

        # Act: Submit an empty comment body,
        # which should not be saved to the database
        response = self.client.post(self.add_comment_url, data={"body": ""})

        # Assert: No new comment was created, so the comment count
        # remains 2 (1 approved, 1 unapproved)
        self.assertEqual(Comment.objects.count(), 2)

        # Assert: The user is redirected back to the event detail page
        self.assertRedirects(response, self.detail_url)


class EditCommentViewTests(TestCase):
    """
    Tests for editing an existing comment.
    """

    def setUp(self):
        """
        Create users, an event and a comment for use in the tests.
        """

        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )

        self.event = Event.objects.create(
            creator=self.other_user,
            title="Test Event",
            slug="test-event",
            description="A test event.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            status=1,
        )

        self.comment = Comment.objects.create(
            event=self.event,
            author=self.user,
            body="Original comment",
            approved=True
        )

        self.edit_url = reverse("edit_comment", args=[self.comment.id])

    def test_comment_author_can_access_edit_page(self):
        """
        Test that the author of a comment can access
        the comment edit page.
        """

        # Arrange: Log in as the comment author.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the comment edit page.
        response = self.client.get(self.edit_url)

        # Assert: The page loads successfully and uses
        # the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/comment_edit.html")

    def test_edit_form_is_prefilled_with_existing_comment(self):
        """
        Test that the edit form is populated with
        the comment's existing body text.
        """

        # Arrange: Log in as the comment author.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the comment edit page.
        response = self.client.get(self.edit_url)

        # Assert: The form contains the existing comment body.
        self.assertContains(response, "Original comment")

    def test_comment_author_can_update_comment(self):
        """
        Test that the comment author can update their existing comment.
        """

        # Arrange: Log in as the comment author.
        self.client.login(username="testuser", password="testpassword")

        # Act: Submit updated comment text.
        response = self.client.post(self.edit_url, {"body": "Updated comment"})

        # Refresh the comment so we have the latest data from the database.
        self.comment.refresh_from_db()

        # Assert: Check the existing comment has been updated.
        self.assertEqual(self.comment.body, "Updated comment")

        # Assert: Check that a new comment has not been created.
        self.assertEqual(Comment.objects.count(), 1)

        # Assert: Check that the user is redirected back to the event detail
        # page.
        self.assertRedirects(response, reverse("event_detail", args=[self.event.slug]))

    def test_non_author_cannot_edit_comment(self):
        """
        Test that a logged-in user cannot edit a comment
        created by another user.
        """

        # Arrange: Log in as a different user.
        self.client.login(username="otheruser", password="testpassword")

        # Act: Attempt to access the edit page.
        response = self.client.get(self.edit_url)

        # Assert: The user is redirected back to the event detail page.
        self.assertRedirects(response, reverse("event_detail", args=[self.event.slug]))

        # Assert: The comment has not been changed.
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, "Original comment")

    def test_logged_out_user_is_redirected_from_edit_comment(self):
        """
        Test that a logged-out user cannot access
        the comment edit page.
        """

        # Act: Attempt to access the edit page without logging in.
        response = self.client.get(self.edit_url)

        # Assert: The user is redirected to the login page.
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.edit_url}"
        )

    def test_invalid_edit_does_not_update_comment(self):
        """
        Test that invalid form data does not update
        the existing comment.
        """

        # Arrange: Log in as the comment author.
        self.client.login(username="testuser", password="testpassword")

        # Act: Submit an empty comment body.
        response = self.client.post(self.edit_url, {"body": ""})

        # Refresh the comment from the database.
        self.comment.refresh_from_db()

        # Assert: The original comment text remains unchanged.
        self.assertEqual(self.comment.body, "Original comment")

        # Assert: The edit page is returned with a form error.
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["comment_form"], "body", "This field is required."
        )


class DeleteCommentViewTests(TestCase):
    """
    Tests for deleting an existing comment.
    """

    def setUp(self):
        """
        Create users, an event and a comment for use in the tests.
        """

        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )

        self.event = Event.objects.create(
            creator=self.other_user,
            title="Test Event",
            slug="test-event",
            description="A test event.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            status=1,
        )

        self.comment = Comment.objects.create(
            event=self.event,
            author=self.user,
            body="Comment to delete",
            approved=True
        )

        self.delete_url = reverse("delete_comment",
                                  args=[self.comment.id]
                                  )

    def test_comment_author_can_access_delete_page(self):
        """
        Test that the comment author can access
        the delete confirmation page.
        """

        # Arrange: Log in as the comment author.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the comment delete page.
        response = self.client.get(self.delete_url)

        # Assert: The page loads successfully and uses
        # the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/comment_delete.html")

    def test_get_request_does_not_delete_comment(self):
        """
        Test that opening the delete confirmation page
        does not delete the comment.
        """

        # Arrange: Log in as the comment author.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the delete confirmation page.
        self.client.get(self.delete_url)

        # Assert: The comment still exists in the database.
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_comment_author_can_delete_comment(self):
        """
        Test that the comment author can delete
        their own comment.
        """

        # Arrange: Log in as the comment author.
        self.client.login(username="testuser", password="testpassword")

        # Act: Submit the delete confirmation form.
        response = self.client.post(self.delete_url)

        # Assert: The comment has been deleted from the database.
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

        # Assert: The user is redirected back to
        # the correct event detail page.
        self.assertRedirects(response, reverse("event_detail",
                                               args=[self.event.slug]
                                               )
                             )

    def test_non_author_cannot_access_delete_page(self):
        """
        Test that another logged-in user cannot access
        the delete confirmation page.
        """

        # Arrange: Log in as a different user.
        self.client.login(username="otheruser", password="testpassword")

        # Act: Attempt to access the delete page.
        response = self.client.get(self.delete_url)

        # Assert: The user is redirected back to
        # the event detail page.
        self.assertRedirects(response, reverse("event_detail",
                                               args=[self.event.slug]
                                               )
                             )

        # Assert: The comment still exists.
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_non_author_cannot_delete_comment(self):
        """
        Test that another logged-in user cannot delete
        a comment created by someone else.
        """

        # Arrange: Log in as a different user.
        self.client.login(username="otheruser", password="testpassword")

        # Act: Attempt to submit directly to the delete URL.
        response = self.client.post(self.delete_url)

        # Assert: The comment has not been deleted.
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

        # Assert: The user is redirected back to
        # the event detail page.
        self.assertRedirects(response, reverse("event_detail",
                                               args=[self.event.slug]
                                               )
                             )

    def test_logged_out_user_is_redirected_from_delete_comment(self):
        """
        Test that a logged-out user cannot access
        the comment delete page.
        """

        # Act: Attempt to access the delete page
        # without logging in.
        response = self.client.get(self.delete_url)

        # Assert: The user is redirected to the login page.
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.delete_url}"
        )

        # Assert: The comment still exists.
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())


# ------------------------------------------------------------
# FAVOURITE VIEW TESTS
# -----------------------------------------------------------


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
            username="favouriteuser", password="testpassword"
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
            status=1,
        )

        # Store the URL for the event detail page and the toggle favourite
        # URL using Django's reverse function. This allows us to refer to the
        # URLs by their names instead of hardcoding them. Allows us to confirm
        # that the user is redirected to the correct page after favouriting or
        # unfavouriting an event.
        self.detail_url = reverse("event_detail", args=[self.event.slug])

        # Store the URL for toggling the favourite status of the event. This
        # URL will be used to test adding and removing the event from the
        # user's favourites.
        self.favourite_url = reverse("toggle_favourite",
                                     args=[self.event.slug]
                                     )

    def test_logged_in_user_can_favourite_an_event(self):
        """
        Test that a logged-in user can add an event to their favourites.
        """
        # Arrange: Log in as the test user
        self.client.login(username="favouriteuser", password="testpassword")

        # Act: Send a POST request to toggle the favourite status of the event
        response = self.client.post(self.favourite_url)

        # Act: Reload the event from the database to ensure the favourite
        # relationship reflects the latest changes after the POST request
        self.event.refresh_from_db()

        # Assert: The user is redirected back to the event detail page
        self.assertRedirects(response, self.detail_url)

        # Assert: The event is now in the user's favourites, proving that
        # the manyto-many relationship between the user and the event was
        # successfully created.
        self.assertTrue(
            self.event.favourited_by.filter(
                id=self.user.id
            ).exists()
        )

    def test_logged_in_user_can_remove_event_from_favourites(self):
        """
        Test that a logged-in user can remove an event from their favourites.
        """

        # Arrange: Log in as the test user
        self.client.login(username="favouriteuser", password="testpassword")

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
            self.event.favourited_by.filter(
                id=self.user.id
            ).exists()
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
            self.event.favourited_by.filter(
                id=self.user.id
            ).exists()
        )

    def test_favourites_are_specific_to_each_user(self):
        """
        Test that favouriting an event only applies to the logged-in user.
        """

        # Arrange: Create a second user so we can verify that favourites
        # are stored separately for each user.
        other_user = User.objects.create_user(
            username="otherfavouriteuser", password="testpassword"
        )

        # Add the event to the original user's favourites, so we can
        # check that the other user does not have it in their favourites.
        self.event.favourited_by.add(self.user)

        # Assert: The original user has favourited the event, showing that
        # the many-to-many relationship is working correctly for that user.
        self.assertTrue(
            self.event.favourited_by.filter(
                id=self.user.id
            ).exists()
        )

        # Assert: The second user has not favourited the event, proving that
        # favouriting is specific to each user and does not affect other users'
        # favourites.
        self.assertFalse(
            self.event.favourited_by.filter(
                id=other_user.id
                ).exists()
            )

    def test_event_detail_shows_correct_favourite_status(self):
        """
        Test that the event detail view correctly identifies
        whether the logged-in user has favourited the event.
        """
        # Arrange: Log in and favourite the event, so we can check that the event detail view
        # correctly identifies the favourite status for the logged-in user.
        self.client.login(username="favouriteuser", password="testpassword")

        # Arrange: Add the event to the user's favourites so the
        # event detail view should recognise it as favourited.
        self.event.favourited_by.add(self.user)

        # Act: Request the event detail page for the event
        response = self.client.get(self.detail_url)

        # Assert: The view passes True for is_favourited in the context,
        # showing that the logged-in user has favourited the event.
        self.assertTrue(response.context["is_favourited"])

    def test_event_detail_shows_unfavourited_status(self):
        """
        Test that the event detail view correctly identifies
        when the logged-in user has not favourited the event.
        """

        # Arrange: Log in as the test user without favouriting the event,
        # so we can check that the event detail view correctly identifies
        # that the event has not been favourited.
        self.client.login(username="favouriteuser", password="testpassword")

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

        # Store the URL for creating a DJ profile using Django's reverse
        # function. This allows us to refer to the URL by its name instead of
        # hardcoding it.
        self.create_url = reverse("dj_profile_create")

    def test_logged_in_user_can_access_dj_profile_create_page(self):
        """
        Test that a logged-in user can access the DJ Profile creation page.
        """
        # Arrange: Log the test user in
        self.client.login(username="djuser", password="testpassword")

        # Act: Request the dj profile creation page, which should be
        # accessible to logged-in users
        response = self.client.get(self.create_url)

        # Assert: The page loads and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_form.html")

    def test_logged_out_user_cannot_access_dj_profile_create_page(self):
        """
        Test that a logged-out user cannot access the dj profile creation page.
        """
        # Act: Request the protected page without logging in, the user should
        # be redirected to the login page
        response = self.client.get(
            self.create_url
            )

        # Assert: The user is redirected to the login page, with a 302 status
        # code and the correct redirect URL
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.create_url}"
        )

    def test_logged_in_user_can_create_dj_profile(self):
        """
        Test that a logged-in user can submit valid data
        and create a new DJ profile.
        """
        # Arrange: Log the user in
        self.client.login(username="djuser", password="testpassword")

        # Arrange: Prepare valid form data for creating a new DJ profile.
        # image, website, and social_media fields
        # not included because they're optional
        form_data = {
            "dj_name": "Test DJ",
            "bio": "A test DJ profile created through the form.",
            "genres": "Test genre",
            "location": "Manchester",
        }

        # Act: Submit the form, which should create a new DJ profile.
        response = self.client.post(self.create_url, data=form_data)

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
        self.client.login(username="djuser", password="testpassword")

        # Arrange: Create an initial DJ profile for the user, so we
        # can test that they cannot create a second one.
        DJProfile.objects.create(
            owner=self.user,
            dj_name="Existing DJ",
            bio="An existing DJ profile.",
            genres="Existing genre",
            location="Manchester",
        )

        # Act: Attempt to create a second DJ profile for the same user
        response = self.client.post(
            self.create_url,
            data={
                "dj_name": "Second DJ",
                "bio": "Attempting to create a second DJ profile.",
                "genres": "Second genre",
                "location": "Liverpool",
            },
        )

        # Assert: The user is redirected to the homepage.
        self.assertRedirects(response, reverse("home"))

        # Assert: No second DJ profile was created.
        self.assertEqual(DJProfile.objects.count(), 1)

        # Assert: A warning message tells the user that they already have
        # a DJ profile.
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
        self.client.login(username="djuser", password="testpassword")

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
        response = self.client.post(self.create_url, data=invalid_form_data)

        # Assert: No DJ profile was created, as the profile count remains 0,
        # proving that invalid form data does not create a new DJ profile.
        self.assertEqual(DJProfile.objects.count(), 0)

        # Assert: The form is redisplayed instead of redirecting.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_form.html")

        # Assert: The DJ name field contains the expected validation error.
        self.assertFormError(
            response.context["form"], "dj_name", "This field is required."
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
            username="djviewer", password="testpassword"
        )

        # Arrange: Create a DJ profile for the test user, which will be used to
        # test viewing DJ profiles.
        self.dj_profile = DJProfile.objects.create(
            owner=self.user,
            dj_name="Test DJ",
            slug="test-dj",
            bio="A DJ profile used for view tests.",
            genres="House, Techno",
            location="Manchester",
            website="https://example.com",
            social_media="https://instagram.com/testdj",
        )

        # Store the URL for the DJ profile list and detail pages using Django's
        # reverse function. This allows us to refer to the URLs by their names
        # instead of hardcoding them.
        self.list_url = reverse("dj_profile_list")

        # Store the URL for the DJ profile detail page using the slug of the
        # created DJ profile.
        self.detail_url = reverse(
            "dj_profile_detail",
            args=[self.dj_profile.slug]
            )

    def test_dj_profile_list_page_loads_successfully(self):
        """
        Test that the DJ profile list page loads successfully and uses the
        correct template.
        """
        # Act: Request the DJ profile list page
        response = self.client.get(self.list_url)

        # Assert: The page loads with a 200 status code and uses the correct
        # template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_list.html")

    def test_dj_profile_list_displays_dj_profile(self):
        """
        Test that a DJ profile is displayed on the DJ profile list page.
        """
        # Act: Request the DJ profile list page
        response = self.client.get(self.list_url)

        # Assert: The page contains the DJ name of the created DJ profile,
        # proving that it is displayed on the list page.
        self.assertContains(response, "Test DJ")

    def test_dj_profile_detail_page_loads_successfully(self):
        """
        Test that a DJ profile detail page loads successfully
        and uses the correct template.
        """
        # Act: Request the DJ profile detail page for the created DJ profile
        response = self.client.get(self.detail_url)

        # Assert: The page loads with a 200 status code and uses the correct
        # template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_detail.html")

    def test_dj_profile_detail_displays_correct_profile(self):
        """
        Test that the DJ profile detail page displays
        the correct DJ profile information.
        """
        # Act: Request the DJ profile detail page for the created DJ profile
        response = self.client.get(self.detail_url)

        # Assert: The page contains the DJ name, bio, genres, location,
        # website, and social media of the created DJ profile, proving that the
        # correct profile information is displayed on the detail page.
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
        response = self.client.get(
            reverse("dj_profile_detail", args=["nonexistent-dj"])
        )

        # Assert: The response status code is 404, showing that the requested
        # DJ profile does not exist.
        self.assertEqual(response.status_code, 404)


class DJProfileEditViewTests(TestCase):
    """
    Tests for editing DJ profiles.
    """

    def setUp(self):
        """
        Create a profile owner, another user, a DJ profile,
        and store the edit and detail URLs.
        """

        # Arrange: Create a test user who owns the DJ profile and can edit it.
        self.owner = User.objects.create_user(
            username="djowner", password="testpassword"
        )

        # Arrange: Create another test user who does not own the DJ profile,
        # to test that only the owner can edit it.
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )

        # Arrange: Create a DJ profile owned by the first user, which will be
        # used to test editing.
        self.dj_profile = DJProfile.objects.create(
            owner=self.owner,
            dj_name="Original DJ",
            slug="original-dj",
            bio="Original DJ bio.",
            genres="House",
            location="Manchester",
            website="https://example.com",
            social_media="https://instagram.com/originaldj",
        )

        # Store the URL for editing the DJ profile using Django's reverse
        # function, which allows us to refer to the URL by its name instead of
        # hardcoding it. This URL will be used to test editing the DJ profile.
        self.edit_url = reverse(
            "dj_profile_edit",
            args=[self.dj_profile.slug]
            )

        # Store the URL for viewing the DJ profile detail page using Django's
        # reverse function, which allows us to refer to the URL by its name
        # instead of hardcoding it.This URL will be used to test viewing 
        # the DJ profile.
        self.detail_url = reverse(
            "dj_profile_detail",
            args=[self.dj_profile.slug]
        )

    def test_owner_can_access_dj_profile_edit_page(self):
        """
        Test that the DJ profile owner can access the edit page.
        """

        # Arrange: Log in as the owner of the DJ profile.
        self.client.login(username="djowner", password="testpassword")

        # Act: Request the DJ profile edit page.
        response = self.client.get(self.edit_url)

        # Assert: The page loads successfully and uses the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_form.html")

    def test_edit_form_is_prefilled_with_existing_profile(self):
        """
        Test that the DJ profile edit form is pre-filled
        with the existing profile data.
        """

        # Arrange: Log in as the owner of the DJ profile.
        self.client.login(username="djowner", password="testpassword")

        # Act: Request the DJ profile edit page.
        response = self.client.get(self.edit_url)

        # Assert: The form is linked to the existing DJ profile instance.
        self.assertEqual(
            # The form instance in the response context should be the same
            # as the DJ profile instance we created in setUp.
            response.context["form"].instance,
            self.dj_profile,
        )

        # Assert: The form contains the existing DJ profile data.
        self.assertEqual(response.context["form"].initial["dj_name"],
                         "Original DJ")

    def test_owner_can_update_dj_profile(self):
        """
        Test that the DJ profile owner can submit valid data
        and update their existing profile.
        """

        # Arrange: Log in as the owner of the DJ profile.
        self.client.login(username="djowner", password="testpassword")

        # Arrange: Prepare valid updated profile data.
        updated_form_data = {
            "dj_name": "Updated DJ",
            "bio": "This DJ profile has been updated.",
            "genres": "Techno, Disco",
            "location": "Liverpool",
            "website": "https://updated-example.com",
            "social_media": "https://instagram.com/updateddj",
        }

        # Act: Submit the updated data to the DJ profile edit view.
        response = self.client.post(self.edit_url, data=updated_form_data)

        # Assert: Editing did not create a second DJ profile, as the count
        # of DJ profiles in the database remains 1, proving that the existing
        # profile was updated instead of creating a new one.
        self.assertEqual(DJProfile.objects.count(), 1)

        # Reload the profile from the database so the instance contains
        # the latest values after the update.
        self.dj_profile.refresh_from_db()

        # Assert: The existing DJ profile and relevant fields were updated
        # successfully.
        self.assertEqual(
            self.dj_profile.bio,
            "This DJ profile has been updated."
            )
        self.assertEqual(
            self.dj_profile.genres,
            "Techno, Disco"
            )
        self.assertEqual(
            self.dj_profile.location,
            "Liverpool"
            )
        self.assertEqual(
            self.dj_profile.website,
            "https://updated-example.com"
        )
        self.assertEqual(
            self.dj_profile.social_media,
            "https://instagram.com/updateddj"
        )
        )

        # Assert: The user is redirected to the updated profile detail page.
        self.assertRedirects(
            response,
            reverse(
                "dj_profile_detail",
                # The slug remains unchanged because the model only generates
                # it when the slug field is empty.
                args=[self.dj_profile.slug],
            ),
        )

    def test_non_owner_cannot_access_dj_profile_edit_page(self):
        """
        Test that a logged-in user cannot edit another user's DJ profile.
        """

        # Arrange: Log in as a different user who does not own the DJ profile.
        self.client.login(username="otheruser", password="testpassword")

        # Act: Attempt to access the DJ profile edit page.
        response = self.client.get(
            self.edit_url
            )

        # Assert: The non-owner is redirected to the DJ profile detail page.
        self.assertRedirects(response, self.detail_url)

    def test_logged_out_user_is_redirected_from_dj_profile_edit_page(self):
        """
        Test that a logged-out user cannot access the DJ profile edit page.
        """

        # Act: Request the DJ profile edit page without logging in.
        response = self.client.get(self.edit_url)

        # Assert: The user is redirected to the login page with the edit URL
        # stored in the next parameter.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.edit_url}"
        )

    def test_invalid_form_does_not_update_dj_profile(self):
        """
        Test that invalid form data does not update the existing DJ profile.
        """

        # Arrange: Log in as the owner of the DJ profile.
        self.client.login(username="djowner", password="testpassword")

        # Arrange: Prepare invalid form data with the required DJ name missing.
        # "" used for dj_name to simulate a user submitting a form without
        # filling in the required field.
        invalid_form_data = {
            "dj_name": "",
            "bio": "This should not be saved.",
            "genres": "Techno",
            "location": "Liverpool",
        }

        # Act: Submit the invalid form data to the edit view.
        response = self.client.post(
            self.edit_url,
            data=invalid_form_data
            )

        # Reload the DJ profile from the database to check that its
        # existing data has not been changed.
        self.dj_profile.refresh_from_db()

        # Assert: The original DJ profile data remains unchanged.
        self.assertEqual(self.dj_profile.dj_name, "Original DJ")
        self.assertEqual(self.dj_profile.bio, "Original DJ bio.")
        self.assertEqual(self.dj_profile.genres, "House")
        self.assertEqual(self.dj_profile.location, "Manchester")

        # Assert: The invalid form is displayed again rather than redirecting.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/dj_profile_form.html")

        # Assert: The DJ name field contains the expected validation error.
        self.assertFormError(
            response.context["form"], "dj_name", "This field is required."
        )


class DJProfileDeleteViewTests(TestCase):
    """
    Tests for deleting DJ profiles.
    """

    def setUp(self):
        """
        Create a DJ profile owner, another user, a DJ profile,
        and store the relevant URLs.
        """

        # Arrange: Create a test user who owns the DJ profile and can delete
        # it.
        self.owner = User.objects.create_user(
            username="djowner", password="testpassword"
        )

        # Arrange: Create another test user who does not own the DJ profile,
        # to test that only the owner can delete it.
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )

        # Arrange: Create a DJ profile owned by the first user, which will be
        # used to test deletion.
        self.dj_profile = DJProfile.objects.create(
            owner=self.owner,
            dj_name="DJ To Delete",
            slug="dj-to-delete",
            bio="A DJ profile used for deletion tests.",
            genres="House",
            location="Manchester",
        )

        # Store the URL for deleting the DJ profile using Django's reverse
        # function, which allows us to refer to the URL by its name instead of
        # hardcoding it.
        self.delete_url = reverse("dj_profile_delete", args=[self.dj_profile.slug])

        # Store the URL for viewing the DJ profile detail page using Django's
        # reverse function, which allows us to refer to the URL by its name
        # instead of hardcoding it.
        self.detail_url = reverse(
            "dj_profile_detail",
            args=[self.dj_profile.slug]
            )

    def test_owner_can_access_delete_confirmation_page(self):
        """
        Test that the DJ profile owner can access
        the delete confirmation page.
        """

        # Arrange: Log in as the owner of the DJ profile.
        self.client.login(username="djowner", password="testpassword")

        # Act: Request the DJ profile delete confirmation page.
        response = self.client.get(self.delete_url)

        # Assert: The page loads successfully and uses the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "events/dj_profile_confirm_delete.html"
            )

    def test_get_request_does_not_delete_dj_profile(self):
        """
        Test that opening the delete confirmation page
        does not delete the DJ profile. Deletion should
        only occur after a POST request, where the user
        confirms they want to delete the profile.
        """

        # Arrange: Log in as the owner of the DJ profile.
        self.client.login(username="djowner", password="testpassword")

        # Act: Request the delete confirmation page using GET.
        response = self.client.get(self.delete_url)

        # Assert: The confirmation page loads successfully.
        self.assertEqual(response.status_code, 200)

        # Assert: The DJ profile still exists in the database,
        # proving that deletion only occurs after a POST request.
        self.assertTrue(
            DJProfile.objects.filter(
                pk=self.dj_profile.pk).exists(
                )
            )

    def test_owner_can_delete_dj_profile(self):
        """
        Test that the DJ profile owner can confirm deletion
        and remove their profile from the database.
        """

        # Arrange: Log in as the owner of the DJ profile.
        self.client.login(username="djowner", password="testpassword")

        # Act: Submit the delete confirmation form using POST.
        response = self.client.post(self.delete_url)

        # Assert: The DJ profile has been deleted from the database,
        # as the count of DJ profiles is now 0.
        self.assertEqual(DJProfile.objects.count(), 0)

        # Assert: The specific DJ profile no longer exists.
        self.assertFalse(
            DJProfile.objects.filter(
                pk=self.dj_profile.pk).exists(
                    )
                )

        # Assert: The user is redirected to the DJ profile list page
        # after successfully deleting their profile.
        self.assertRedirects(response, reverse("dj_profile_list"))

    def test_non_owner_cannot_delete_dj_profile(self):
        """
        Test that a logged-in user cannot delete
        another user's DJ profile.
        """

        # Arrange: Log in as a different user who does not own the DJ profile.
        self.client.login(username="otheruser", password="testpassword")

        # Act: Attempt to delete another user's DJ profile using POST.
        response = self.client.post(self.delete_url)

        # Assert: The DJ profile still exists in the database,
        # proving that the non-owner was not allowed to delete it.
        self.assertTrue(
            DJProfile.objects.filter(
                pk=self.dj_profile.pk).exists(
                    )
                )

        # Assert: The non-owner is redirected to the DJ profile detail page.
        self.assertRedirects(response, self.detail_url)

    def test_logged_out_user_is_redirected_from_dj_profile_delete_page(self):
        """
        Test that a logged-out user cannot access
        the DJ profile delete page.
        """

        # Act: Request the DJ profile delete page without logging in.
        response = self.client.get(self.delete_url)

        # Assert: The user is redirected to the login page with the delete
        # URL stored in the next parameter.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.delete_url}"
        )

        # Assert: The DJ profile still exists in the database.
        self.assertTrue(
            DJProfile.objects.filter(
                pk=self.dj_profile.pk).exists(
                )
            )

    def test_non_owner_cannot_access_delete_confirmation_page(self):
        """
        Test that a logged-in non-owner cannot access
        another user's DJ profile delete confirmation page.
        """

        # Arrange: Log in as a different user who does not own the DJ profile.
        self.client.login(username="otheruser", password="testpassword")

        # Act: Attempt to open the delete confirmation page.
        response = self.client.get(self.delete_url)

        # Assert: The non-owner is redirected to the DJ profile detail page.
        self.assertRedirects(response, self.detail_url)

        # Assert: The DJ profile still exists in the database.
        self.assertTrue(
            DJProfile.objects.filter(
                pk=self.dj_profile.pk).exists(
                )               
            )


class DJProfileSearchTests(TestCase):
    """
    Tests for searching DJ profiles.
    """

    def setUp(self):
        """
        Create DJ profiles with different names,
        genres and locations for search testing.
        """

        self.user_one = User.objects.create_user(
            username="djone", password="testpassword"
        )

        self.user_two = User.objects.create_user(
            username="djtwo", password="testpassword"
        )
        # Arrange: Create a DJ profile with the below attributes to test the
        # search function.
        self.profile_one = DJProfile.objects.create(
            owner=self.user_one,
            dj_name="Neon Pulse",
            slug="neon-pulse",
            bio="Manchester house DJ.",
            genres="House",
            location="Manchester",
        )
        # Arrange: Create a second DJ profile with different attributes to test
        # search function.
        self.profile_two = DJProfile.objects.create(
            owner=self.user_two,
            dj_name="Bass Theory",
            slug="bass-theory",
            bio="Bristol techno DJ.",
            genres="Techno",
            location="Bristol",
        )

        self.list_url = reverse("dj_profile_list")

    def test_search_by_dj_name(self):
        """
        Test that DJ profiles can be searched by DJ name.
        """

        response = self.client.get(self.list_url, {"q": "Neon"})

        self.assertContains(response, "Neon Pulse")
        self.assertNotContains(response, "Bass Theory")

    def test_search_by_genre(self):
        """
        Test that DJ profiles can be searched by genre.
        """

        response = self.client.get(self.list_url, {"q": "House"})

        self.assertContains(response, "Neon Pulse")
        self.assertNotContains(response, "Bass Theory")

    def test_search_by_location(self):
        """
        Test that DJ profiles can be searched by location.
        """

        response = self.client.get(self.list_url, {"q": "Bristol"})

        self.assertContains(response, "Bass Theory")
        self.assertNotContains(response, "Neon Pulse")

    def test_search_is_case_insensitive(self):
        """
        Test that DJ search is not case-sensitive.
        """

        response = self.client.get(self.list_url, {"q": "manchester"})

        self.assertContains(response, "Neon Pulse")

    def test_search_with_no_results_displays_message(self):
        """
        Test that an appropriate message is displayed
        when no DJ profiles match the search query.
        """

        response = self.client.get(self.list_url, {"q": "Drum and Bass"})

        self.assertContains(response, 'No DJs found matching "Drum and Bass".')

    def test_empty_search_displays_all_profiles(self):
        """
        Test that an empty search displays all DJ profiles.
        """

        response = self.client.get(self.list_url, {"q": ""})

        self.assertContains(response, "Neon Pulse")
        self.assertContains(response, "Bass Theory")


class FavouriteEventsViewTests(TestCase):
    """
    Tests for viewing a logged-in user's favourite events.
    """

    def setUp(self):
        """
        Create two users and published events for testing
        the favourite events page.
        """

        # Arrange: Create the user whose favourites will be tested.
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Arrange: Create another user to ensure favourites
        # belonging to different users are not displayed.
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )

        # Arrange: Create an event that will be favourited by the test user.
        self.favourite_event = Event.objects.create(
            creator=self.other_user,
            title="Favourite Event",
            slug="favourite-event",
            description="An event saved as a favourite.",
            venue="Favourite Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            status=1,
        )

        # Arrange: Create another event that has not been favourited.
        self.other_event = Event.objects.create(
            creator=self.other_user,
            title="Other Event",
            slug="other-event",
            description="An event that has not been favourited.",
            venue="Other Venue",
            location="London",
            date=timezone.now(),
            genre="Techno",
            status=1,
        )

        # Add only the first event to the user's favourites.
        self.favourite_event.favourited_by.add(self.user)

        # Store the URL for the favourite events page.
        self.favourites_url = reverse("favourite_events")

    def test_logged_in_user_can_access_favourites_page(self):
        """
        Test that a logged-in user can access
        the My Favourites page.
        """

        # Arrange: Log in as the test user, as the favourite_events view has
        # @login_required decorator,which requires the user to be logged in to
        # access the page.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the My Favourites page.
        response = self.client.get(self.favourites_url)

        # Assert: The page loads successfully and uses the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/favourite_events.html")

    def test_logged_out_user_is_redirected_from_favourites_page(self):
        """
        Test that a logged-out user cannot access
        the My Favourites page.
        """

        # Act: Request the My Favourites page without logging in.
        response = self.client.get(self.favourites_url)

        # Assert: The user is redirected to the login page with the
        # favourites URL stored in the next parameter.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={self.favourites_url}"
        )

    def test_favourites_page_displays_users_favourite_event(self):
        """
        Test that an event favourited by the logged-in user
        is displayed on their My Favourites page.
        """

        # Arrange: Log in as the test user.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the My Favourites page.
        response = self.client.get(self.favourites_url)

        # Assert: The user's favourited event is displayed.
        self.assertContains(response, "Favourite Event")

    def test_favourites_page_does_not_display_non_favourite_event(self):
        """
        Test that an event not favourited by the logged-in user
        is not displayed on their My Favourites page.
        """

        # Arrange: Log in as the test user.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the My Favourites page.
        response = self.client.get(self.favourites_url)

        # Assert: The event that has not been favourited is not displayed.
        self.assertNotContains(response, "Other Event")

    def test_favourites_page_shows_message_when_user_has_no_favourites(self):
        """
        Test that an appropriate message is displayed
        when the logged-in user has no favourite events.
        """

        # Arrange: Remove the event from the user's favourites
        # so that the user has no favourite events.
        self.favourite_event.favourited_by.remove(self.user)

        # Arrange: Log in as the test user.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the My Favourites page.
        response = self.client.get(self.favourites_url)

        # Assert: The empty favourites message is displayed.
        self.assertContains(
            response,
            "You have not added any favourite events yet."
            )

    def test_favourite_event_links_to_correct_detail_page(self):
        """
        Test that a favourited event links to its
        corresponding event detail page.
        """

        # Arrange: Log in as the test user.
        self.client.login(username="testuser", password="testpassword")

        # Act: Request the My Favourites page.
        response = self.client.get(self.favourites_url)

        # Arrange: Build the expected detail URL for the favourited event.
        expected_url = reverse(
            "event_detail",
            args=[self.favourite_event.slug]
            )

        # Assert: The response contains a link to the correct event detail
        # page.
        self.assertContains(response, f'href="{expected_url}"')


class Custom404Tests(TestCase):
    """
    Tests for the custom 404 error page.
    """

    def test_invalid_url_returns_404_status(self):
        """
        Test that requesting a non-existent URL
        returns a 404 HTTP status.
        """

        # Act: Request a URL that does not exist.
        response = self.client.get("/this-page-does-not-exist/")

        # Assert: The response has a 404 status code.
        self.assertEqual(response.status_code, 404)

    def test_custom_404_template_is_used(self):
        """
        Test that the custom 404 template is displayed
        for a non-existent URL.
        """

        # Act: Request a URL that does not exist.
        response = self.client.get("/this-page-does-not-exist/")

        # Assert: The custom 404 template is used.
        self.assertTemplateUsed(response, "404.html")

    def test_custom_404_contains_return_home_link(self):
        """
        Test that the custom 404 page contains
        a link back to the homepage.
        """

        # Act: Request a URL that does not exist.
        response = self.client.get("/this-page-does-not-exist/")

        # Assert: The response contains the homepage URL.
        self.assertContains(response, reverse("home"), status_code=404)


# -------------------------------------------------------------
# DASHBOARD TESTS
# -------------------------------------------------------------


class DashboardTests(TestCase):
    """
    Tests for the logged-in user's dashboard.
    """

    def setUp(self):
        """
        Create users, DJ profiles and events for dashboard testing.
        """

        self.user_one = User.objects.create_user(
            username="userone", password="testpassword"
        )

        self.user_two = User.objects.create_user(
            username="usertwo", password="testpassword"
        )

        # Create a DJ profile belonging to user one.
        self.profile_one = DJProfile.objects.create(
            owner=self.user_one,
            dj_name="DJ One",
            slug="dj-one",
            bio="Test DJ profile.",
            genres="House",
            location="Manchester",
        )

        # Create an event belonging to user one.
        self.event_one = Event.objects.create(
            creator=self.user_one,
            title="User One Event",
            slug="user-one-event",
            description="An event created by user one.",
            venue="Test Venue",
            location="Manchester",
            date=timezone.now(),
            genre="House",
            lineup="DJ One",
            status=1,
        )

        # Create an event belonging to user two.
        self.event_two = Event.objects.create(
            creator=self.user_two,
            title="User Two Event",
            slug="user-two-event",
            description="An event created by user two.",
            venue="Another Venue",
            location="Bristol",
            date=timezone.now(),
            genre="Techno",
            lineup="DJ Two",
            status=1,
        )

        self.dashboard_url = reverse("dashboard")

    def test_logged_out_user_is_redirected_to_login(self):
        """
        Test that a logged-out user cannot access the dashboard.
        """
        # Act: Request the dashboard page without logging in.
        response = self.client.get(self.dashboard_url)

        # Assert: The user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_user_sees_own_dj_profile(self):
        """
        Test that the logged-in user's DJ profile is displayed.
        """
        # Arrange: Log in as user one, who has a DJ profile.
        self.client.login(username="userone", password="testpassword")
        # Act: Request the dashboard page.
        response = self.client.get(self.dashboard_url)
        # Assert: The response contains the DJ name of the logged-in user's
        # profile.
        self.assertContains(response, "DJ One")

    def test_user_sees_own_events(self):
        """
        Test that events created by the logged-in user are displayed.
        """
        # Arrange: Log in as user one, who has created an event.
        self.client.login(username="userone", password="testpassword")
        # Act: Request the dashboard page.
        response = self.client.get(self.dashboard_url)

        # Assert: The response contains the event created by the logged-in
        # user.
        self.assertContains(response, "User One Event")

    def test_user_does_not_see_another_users_events(self):
        """
        Test that events created by another user are not displayed
        in the My Events section.
        """
        # Arrange: Log in as user one, but the event belongs to user two.
        self.client.login(username="userone", password="testpassword")
        # Act: Request the dashboard page.
        response = self.client.get(self.dashboard_url)

        # Assert: The response does not contain the event created by another
        # user.
        self.assertNotContains(response, "User Two Event")

    def test_user_sees_favourite_events(self):
        """
        Test that events favourited by the logged-in user are displayed.
        """
        # Arrange: Add the event created by user two to user one's favourites.
        self.event_two.favourited_by.add(self.user_one)
        # Arrange: Log in as user one
        self.client.login(username="userone", password="testpassword")
        # Act: Request the dashboard page.
        response = self.client.get(self.dashboard_url)
        # Assert: The response contains the event favourited by the logged-in
        # user.
        self.assertContains(response, "User Two Event")

    def test_dashboard_loads_without_dj_profile(self):
        """
        Test that the dashboard still loads if the logged-in
        user does not have a DJ profile.
        """
        # Arrange: Log in as user two, who does not have a DJ profile.
        self.client.login(username="usertwo", password="testpassword")
        # Act: Request the dashboard page.
        response = self.client.get(self.dashboard_url)
        # Assert: The dashboard loads successfully and displays a message
        # indicating that
        # the user has not created a DJ profile yet.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have not created a DJ profile yet.")

    def test_dashboard_loads_without_events_or_favourites(self):
        """
        Test that the dashboard still loads if the user
        has no created events or favourite events.
        """
        # Arrange: Create a new user who has not created any events or
        # favourited any events.
        user_three = User.objects.create_user(
            username="userthree", password="testpassword"
        )
        # Arrange: Log in as the new user.
        self.client.login(username="userthree", password="testpassword")
        # Act: Request the dashboard page.
        response = self.client.get(self.dashboard_url)
        # Assert: The dashboard loads successfully
        self.assertEqual(response.status_code, 200)
        # Assert: The response contains the message indicating that the user
        # has not created any events yet.
        self.assertContains(response, "You have not created any events yet.")
        # Assert: The page shows a message because the user
        # has not favourited any events yet.
        self.assertContains(
            response,
            "You have not favourited any events yet."
        )