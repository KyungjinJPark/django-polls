from typing import Any
from django.db.models.query import QuerySet
from django.utils import timezone
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    # default template_name is `polls/question_list.html`
    context_object_name = "latest_question_list" # default question_list

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to
        be published in the future)
        """ # documentation
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    # default template_name is `polls/question_detail.html`
    model = Question # derives default context_object_name
    def get_queryset(self) -> QuerySet[Any]:
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question # derives default context_object_name
    template_name = "polls/results.html" # polls/templates/ prepended to template for namespace

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # re-display the question voting form
        return render(request, "polls/detail.html", { "question": question, "error_message": "You didn't display a choice." })
    else:
        # add one to the votes
        selected_choice.votes = F("votes") + 1 # prevents race conditions
        selected_choice.save() # performs the function
        # selected_choice.save() # !! if run, will perform the function again
        # Redirects prevents data from double posting if the back button is hit
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,))) # reverse gets the url given the view name & params # , makes it a tuple
