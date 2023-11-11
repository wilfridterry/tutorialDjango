import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self) -> None:
        """
        was_published_recently() returns False 
        for questions whose published_at is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(published_at=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self) -> None:
        """
        was_published_recently() returns False 
        for questions whose published_at is in the past, more than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(published_at=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        """
        was_published_recently() returns True 
        for questions whose published_at is in less than 1 day
        """
        recent_question = Question(published_at=timezone.now())
        self.assertIs(recent_question.was_published_recently(), True)



def create_question(text: str, days: int, num_choices: int=None) -> Question:
    """
    Creates a question with the given and the number of days
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(text=text, published_at=time)
    if num_choices:
        for i in range(num_choices):
            question.choice_set.create(text=f"Choice {i}")
    return question

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


class QuestionDetailViewTests(TestCase):
    def test_future_question(self) -> None:
        """
        The detail veiw of question with a published_at in the future
        returns a 404 not found
        """
        future_question = create_question(text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_without_choices(self) -> None:
        """
        The detail veiw of question with a published_at in the past
        and without choices doesn't display the question detail template
        """
        past_question = create_question(text="Future question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_with_choices(self) -> None:
        """
        The detail veiw of question with a published_at in the past
         and wit choices displays the question detail template
        """
        past_question = create_question(text="Future question.", days=-5, num_choices=3)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.text)

class QuestionResultsViewTests(TestCase):
    def test_future_question(self) -> None:
        """
        The results veiw of question with a published_at in the future
        returns a 404 not found
        """
        future_question = create_question(text="Future question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    
    def test_past_question_without_choices(self) -> None:
        """
        The detail veiw of question with a published_at in the past
        and without choices doesn't display the question results template
        """
        past_question = create_question(text="Future question.", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_with_choices(self) -> None:
        """
        The detail veiw of question with a published_at in the past
         and wit choices displays the question results template
        """
        past_question = create_question(text="Future question.", days=-5, num_choices=3)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.text)