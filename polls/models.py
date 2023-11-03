from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin


# Create your models here.
#   Two models: Question and Choice.
#       A Question has a question and a publication date.
#       A Choice has two fields: the text of the choice and a vote tally. Each Choice is associated with a Question.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # return False if the pub_date is in the future.
    # Amended so that it will only return True if the date is also in the past
    # @admin.display(...) modifies the name of the boolean fields from 'WAS PUBLISHED RECENTLY' to 'Published recently?'
    # and changes the boolean values from True/False to red 'X' and green 'checkmark' icons on the admin page
    @admin.display(boolean=True, ordering="pub_date", description="Published recently?",)
    def was_published_recently(self):
        # return self.pub_date >= (timezone.now() - datetime.timedelta(days=1))
        return (timezone.now() - datetime.timedelta(days=1)) <= self.pub_date <= timezone.now()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # defines a relationship using the ForeignKey. It tells Django that each Choice is related to a single Question
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
