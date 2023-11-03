from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # """Return the last 5 published questions."""
        # return Question.objects.order_by("-pub_date")[:5]
        """
        Return the last five published questions (not including those set to be published in the future).

        Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing Questions whose pub_date
        is less than or equal to - that is, earlier than or equal to - timezone.now()
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

        # """Exclude any questions without choices."""
        # return [question for question in Question.objects.all() if question.choice_set.count() != 0]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """ Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/result.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


"""
    # Original Views (before using Generic Views)
    # -------------------------------------------
# Question "index" page - displays the latest few questions.
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     return render(request, "polls/index.html", {"latest_question_list": latest_question_list, })


# Question "detail" page - displays a question text, with no results but with a form to vote.
# def detail(request, question_id):
    # # less efficient way to rewrite active code below
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, "polls/detail.html", {"question": question})

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# Question "results" page - displays results for a particular question.
# After someone votes on a question, the vote() view redirects to the results page for that question.
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/result.html", {"question": question})
"""


# Vote action - handles voting for a particular choice in a particular question
def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        context = {
            "question": question,
            "error_message": "You didn't select a choice.",
        }
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


"""
This code includes a few things we haven’t covered yet in this tutorial:

request.POST is a dictionary-like object that lets you access submitted data by key name. In this case, 
request.POST['choice'] returns the ID of the selected choice, as a string. request.POST values are always strings.

Note that Django also provides request.GET for accessing GET data in the same way – but we’re explicitly using 
request.POST in our code, to ensure that data is only altered via a POST call.

request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. The above code checks for KeyError 
and redisplays the question form with an error message if choice isn’t given.

After incrementing the choice count, the code returns an HttpResponseRedirect rather than a normal HttpResponse. 
HttpResponseRedirect takes a single argument: the URL to which the user will be redirected (see the following point 
for how we construct the URL in this case).

As the Python comment above points out, you should always return an HttpResponseRedirect after successfully dealing 
with POST data. This tip isn’t specific to Django; it’s good web development practice in general.

We are using the reverse() function in the HttpResponseRedirect constructor in this example. This function helps avoid 
having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the 
variable portion of the URL pattern that points to that view. In this case, using the URLconf we set up in Tutorial 3, 
this reverse() call will return a string like:

    "/polls/3/results/"
    
where the 3 is the value of question.id. This redirected URL will then call the 'results' view to display the final page.
"""
