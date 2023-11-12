from django.test import TestCase
from django.urls import reverse

from polls.tests.utils import create_question


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self) -> None:
        """
        If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question(self) -> None:
        """
        Questions with a published_at in the future aren't displayed on the index page
        """
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question_without_choices(self) -> None:
        """
        Questions with a published_at in the past without choices
        aren't displayed on the index page
        """

        question = create_question("Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")

        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question_with_choices(self) -> None:
        """
        Questions with a published_at in the past with choices 
        are displayed on the index page
        """

        question = create_question("Past question.", days=-30, num_choices=3)
        response = self.client.get(reverse("polls:index"))
        
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_future_question_and_past_question_without_choices(self) -> None:
        """
        Even if both past and future questions exist but a past without choices
        they aren't displayed
        """
        create_question("Past question.", days=-30)
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    
    def test_future_question_and_past_question_with_choices(self) -> None:
        """
        Even if both past and future questions exist but a past without choices
        they aren't displayed
        """
        question = create_question("Past question.", days=-30, num_choices=3)
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_two_past_qustions_with_choices(self) -> None:
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(text="Past question 1.", days=-10, num_choices=3)
        question2 = create_question(text="Past question 2.", days=-5, num_choices=3)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1]
        )
