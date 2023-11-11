from typing import Any
from django.db import models

from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet[Question]:
        """
        Returns the last five published questions(not including those set
        to be published in the future)
        """
        return (Question.objects
                .distinct()
                .filter(published_at__lte=timezone.now(), choice__isnull=False)
                .order_by("-published_at")[:5])


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self) -> QuerySet[Question]:
        """
        Excludes any questions that haven't published yet
        """
        return (Question.objects
                .distinct()
                .filter(published_at__lte=timezone.now(), choice__isnull=False))

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self) -> QuerySet[Question]:
        """
        Excludes any questions that haven't published yet
        """
        return (Question.objects
                .distinct()
                .filter(published_at__lte=timezone.now(), choice__isnull=False))


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice"
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

