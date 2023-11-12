import datetime

from django.utils import timezone

from polls.models import Question


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