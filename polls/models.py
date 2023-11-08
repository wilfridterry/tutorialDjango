import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.CharField(max_length=255)
    published_at = models.DateTimeField("published at")

    def __str__(self) -> str:
        return self.text
    
    def was_published_recently(self) -> bool:
        return self.published_at >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.text

