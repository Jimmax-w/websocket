from django.urls import path
from celeryapp.views import CeleryView

urlpatterns = [
    path('launch/', CeleryView.as_view()),
]
