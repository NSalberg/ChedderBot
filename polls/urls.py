from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("phone_input/", views.phone_input, name="phone_input"),
    path("thanks/", views.thanks, name="thanks"),
    path("delete/<int:phone_number>/<uuid:UID>", views.delete, name="delete") # type: ignore
]