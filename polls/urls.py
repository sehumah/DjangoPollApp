from django.urls import path
from polls import views


# set the polls application's namespace
app_name = "polls"


urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),  # args: route, view & name
    # ex: /polls/5/detail/        - the 'name' value is called by the {% url %} template tag
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
