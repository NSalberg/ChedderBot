from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("phone_input/", views.phone_input, name="phone_input"),
    path("thanks/", views.thanks, name="thanks"),
    path("delete/<int:phone_number>/<uuid:UID>", views.delete, name="delete") # type: ignore
]