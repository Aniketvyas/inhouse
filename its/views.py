from django.shortcuts import render
from django.contrib.auth.models import User , Group
from django.core.mail import send_mail
import smtplib
# Create your views here.



def index(request):
    return render(request,'its/dashboard.html')

def users(request):
    users = Group.objects.all()
    return render(request,'its/users.html',{'users':users})

def CreateUser(request):
    return render(request,'its/users.html',{'registration':5})

def ExistingUser(request):
    context = {
        'userss' : User.objects.all()
    }
    return render(request,'its/users.html',context)

def GroupBasedUser(request,id):
    context = {
        'userss' : User.objects.filter(groups=id)
    }
    return render(request,'its/users.html',context)


def NonActiveUsers(request):
    context={
        'nonActiveUsers' : User.objects.filter(is_active=False)
    }
    print(User.objects.filter(is_active=True))
    return render(request,'its/users.html',context)

def requestmodule(request):
    send_mail('hello world','automayted meddage','vyasaniket6@gmail.com',['aniket.vyas@spsu.ac.in'],fail_silently=False)
