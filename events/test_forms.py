from django.test import TestCase

from .forms import CommentForm, DJProfileForm, EventForm


class EventFormTests(TestCase):
    """
    Tests for the EventForm.
    """

    def test_event_form_is_valid_with_correct_data(self):
        """
        Test that the event form accepts valid event data.
        """
        # Arrange: Create a dictionary containing valid data for all of the
        # required fields in the event form.
        form_data = {
            "title": "Test Event",
            "description": "This is a test event.",
            "venue": "Test Venue",
            "location": "Manchester",
            "date": "2026-08-20T21:00",
            "genre": "House",
            "lineup": "DJ Test",
        }

        # Act: Pass the test data into the EventForm.
        form = EventForm(data=form_data)

        # Assert: Check that the form accepts the valid data.
        self.assertTrue(form.is_valid())

    def test_event_form_is_invalid_without_title(self):
        """
        Test that the event form requires a title.
        """
        # Arrange: Create otherwise valid event data but leave the title empty.
        form_data = {
            "title": "",
            "description": "This is a test event.",
            "venue": "Test Venue",
            "location": "Manchester",
            "date": "2026-08-20T21:00",
            "genre": "House",
            "lineup": "DJ Test",
        }

        # Act: Pass the test data into the EventForm.
        form = EventForm(data=form_data)

        # Assert: Check that the form is invalid because the required
        # title field has not been completed.
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_event_form_accepts_datetime_local_format(self):
        """
        Test that the date field accepts the datetime-local input format.
        """
        # Arrange: Create valid event data using the same date format
        # submitted by the datetime-local field in the event form.
        form_data = {
            "title": "Test Event",
            "description": "This is a test event.",
            "venue": "Test Venue",
            "location": "Manchester",
            "date": "2026-08-20T21:00",
            "genre": "Techno",
            "lineup": "",
        }

        # Act: Pass the data into the EventForm.
        form = EventForm(data=form_data)

        # Assert: Check that the customised date format is accepted.
        self.assertTrue(form.is_valid())


class CommentFormTests(TestCase):
    """
    Tests for the CommentForm.
    """

    def test_comment_form_is_valid_with_body(self):
        """
        Test that the comment form accepts a valid comment.
        """
        # Arrange: Create valid data containing text for the comment body.
        form_data = {
            "body": "This is a test comment."
        }

        # Act: Pass the test data into the CommentForm.
        form = CommentForm(data=form_data)

        # Assert: Check that the form accepts the valid comment.
        self.assertTrue(form.is_valid())

    def test_comment_form_is_invalid_without_body(self):
        """
        Test that the comment form requires a comment body.
        """
        # Arrange: Create comment data with an empty body.
        form_data = {
            "body": ""
        }

        # Act: Pass the empty data into the CommentForm.
        form = CommentForm(data=form_data)

        # Assert: Check that the form is invalid because the required
        # comment body has not been completed.
        self.assertFalse(form.is_valid())
        self.assertIn("body", form.errors)


class DJProfileFormTests(TestCase):
    """
    Tests for the DJProfileForm.
    """

    def test_dj_profile_form_is_valid_with_correct_data(self):
        """
        Test that the DJ profile form accepts valid profile data.
        """
        # Arrange: Create valid data for all of the DJ profile fields.
        form_data = {
            "dj_name": "DJ Pulse",
            "bio": "Manchester based house DJ.",
            "genres": "House, Techno",
            "location": "Manchester",
            "website": "https://example.com",
            "social_media": "https://instagram.com/djpulse",
        }

        # Act: Pass the test data into the DJProfileForm.
        form = DJProfileForm(data=form_data)

        # Assert: Check that the form accepts the valid DJ profile data.
        self.assertTrue(form.is_valid())

    def test_dj_profile_form_is_invalid_without_dj_name(self):
        """
        Test that the DJ profile form requires a DJ name.
        """
        # Arrange: Create otherwise valid DJ profile data but leave
        # the required DJ name field empty.
        form_data = {
            "dj_name": "",
            "bio": "Manchester based house DJ.",
            "genres": "House",
            "location": "Manchester",
            "website": "",
            "social_media": "",
        }

        # Act: Pass the test data into the DJProfileForm.
        form = DJProfileForm(data=form_data)

        # Assert: Check that the form is invalid and an error is returned
        # against the missing DJ name field.
        self.assertFalse(form.is_valid())
        self.assertIn("dj_name", form.errors)

    def test_dj_profile_form_rejects_invalid_website_url(self):
        """
        Test that the DJ profile form rejects an invalid website URL.
        """
        # Arrange: Create DJ profile data containing an invalid website URL.
        form_data = {
            "dj_name": "DJ Pulse",
            "bio": "Manchester based house DJ.",
            "genres": "House",
            "location": "Manchester",
            "website": "not-a-valid-url",
            "social_media": "",
        }

        # Act: Pass the test data into the DJProfileForm.
        form = DJProfileForm(data=form_data)

        # Assert: Check that Django's URLField validation rejects the
        # incorrectly formatted website address.
        self.assertFalse(form.is_valid())
        self.assertIn("website", form.errors)
