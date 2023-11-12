import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


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

