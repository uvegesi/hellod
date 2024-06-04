from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest_questions_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("poll/index.html")
    context = {
        "latest_question_list": latest_questions_list
    }
    return render(request, "poll/index.html", context)

def detail(request, question_id):
    try:
        # question = Question.objects.get(pk=question_id)
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist.')
    return render(request, "poll/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "poll/results.html", {"question": question})

def vote(request, question_id):
    # return HttpResponse("You are voting in question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "poll/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice."
            }
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("poll:results", args=(question_id,)))
