from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('users',views.users),
    path('CreateUser',views.CreateUser),
    path('ExistingUsers',views.ExistingUser),
    path('<int:id>',views.GroupBasedUser),
    path('NonActiveUsers',views.NonActiveUsers),
    path('Request',views.requestmodule)
]