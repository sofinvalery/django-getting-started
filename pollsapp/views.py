from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from .models import Question, Choice
from django.db.models import F
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = "pollsapp/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "pollsapp/detail.html"
    def get_queryset(self):
       """ Excludes any questions that aren't published yet. """
       return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "pollsapp/results.html"

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try: selected_choice = question.choice_set.get(pk=request.POST["choice"])
  except (KeyError, Choice.DoesNotExist):
    return render(
      request,
      "pollsapp/detail.html", {
        "question" : question,
        "error_message" : "You didn't select a choice.",
      },
    )
  else:
    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse("pollsapp:results", args=(question_id,)))