from django.shortcuts import render,redirect
from academics.models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Create your views here.
import json



def lecture(request):
    lectures = lectureEnrollment.objects.filter(studentID = stud_details.objects.get(UniversityEmailID=request.user))
    return render(request,'student/lecture.html',{'lecture':lectures})


def track(request,lecture):
    obj = lectureRecord.objects.filter(lectureId=lectures.objects.get(LectureID=lecture))
    return render(request,'bs4_Horizontal_timeline.html',{'track':obj,'student':True})