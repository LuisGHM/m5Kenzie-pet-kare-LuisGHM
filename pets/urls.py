from django.urls import path
from .views import PetView, petIdView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", petIdView.as_view())
]