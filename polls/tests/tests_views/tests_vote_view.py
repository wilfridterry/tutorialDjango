from django.test import TestCase
from django.urls import reverse

from polls.tests.utils import create_question


class VoteViewsTests(TestCase):
    def test_future_qeustion(self): 
        question = create_question("Question.", 30)
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)), 
            {'choice': 1}
        )

        self.assertEqual(response.status_code, 404)

    def test_undefined_choice(self):
        question = create_question("Question.", -5)
        response = self.client.post(reverse("polls:vote", args=(question.id,)))
        
        self.assertEqual(response.context["error_message"], "You didn't select a choice")

    def test_unexist_choice(self):
        question = create_question("Question.", -5)
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {'choice': 1} 
        )
        
        self.assertEqual(response.context["error_message"], "You didn't select a choice")

    def test_exist_choice(self):
        question = create_question("Question.", -5, num_choices=2)
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {'choice': question.choice_set.all()[0].id} 
        )

        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))