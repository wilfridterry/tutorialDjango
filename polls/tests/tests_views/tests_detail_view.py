from django.test import TestCase
from django.urls import reverse

from polls.tests.utils import create_question


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