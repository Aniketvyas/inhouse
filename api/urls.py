from django.contrib import admin
from django.urls import path,include
from . import views
from .auth import CustomAuthToken


urlpatterns = [

    path('gettoken/',CustomAuthToken.as_view()),
    path('',views.index),
    path('account/',include('accounts.urls')),
    
    # for school
    path('school/',views.schoolView),       # GET: to show all school , POST: add a school
    path('school/<int:id>/', views.delete_school),      #to delete school with id
    path('school/<int:id>/dean/', views.update_dean),   # GET: To show dean , POST: to update dean

    # for Programs
    path('school/<int:id>/program/',views.programView),     # GET: to show all programs , POST: add a program
    path('program/<int:id>/',views.delete_program),     # to delete program
    

    # for department
    path('program/<int:id>/department/',views.departmentView),      # GET: to show all departments , POST: add a department
    path('department/<int:id>/',views.delete_department),       # to delete department
    path('department/<int:id>/hod/',views.update_hod),          # GET: To show hod , POST: to update hod

    # for lectures
    path('department/<int:id>/lecture/',views.lecture),         # GET: to show all lectures , POST: add a lecture
    path('lecture/<int:id>/faculty',views.update_faculty),      # GET: To show faculty , POST: to update faculty
    path('lecture/<int:id>/',views.delete_lecture),             # to delete lecture
    path('lecture/<int:id>/student',views.student),             # GET: to show all student , POST: add a student
    path('student/<int:id>/',views.delete_student),             # to delete student
    path('studentQuizInfo/<str:id>',views.studentQuizInfo),

]
