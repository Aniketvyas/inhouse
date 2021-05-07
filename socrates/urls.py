from django.urls import path
from . import views

urlpatterns = [
    path('lecture',views.lecture),
    path('<str:lecture>/Track',views.track)
]