from django.shortcuts import render , redirect 
from django.contrib.auth.models import User , auth , Group
from django.http import HttpResponse
# from outpass.models import stud_outing ,Warden ,  stud_board , Hostel
from django.contrib import messages
from . import models
import datetime as dt
from datetime import *
import random
from django.shortcuts import get_object_or_404  
from django.contrib.auth.decorators import login_required
from academics.models import employee , stud_details


# Create your views here.


#-----------------------------Login Logout-----------------------------------------#



def login(request):
    print('login')
    if request.method=='POST':
        username = request.POST['email']
        password = request.POST['Password']
        user = auth.authenticate(username=username,password=password)
        a = employee.objects.filter(employeeID=username)
        for i in a:
            a = i.Etype
            print("a",a)
        print(user , username,password)
        # print(type(Group.objects.get(user=User.objects.get(username=username))),Group.objects.get(user=User.objects.get(username=username)) == "guard")
        if user is not None:
            print(user)
            auth.login(request,user)
            group = User.objects.get(username=username).groups.all()
            print(group)
            return redirect('/academic/dashboard')
        else:
            messages.info(request,'Invalid credentials') 
            return redirect('/')   
    else:
        print(request.user.is_superuser)
        if request.user.is_authenticated and request.user.is_superuser != True:
            return redirect('academic/dashboard')
        return render(request,'index.html')    

def logout(request):
    auth.logout(request)
    return redirect('/')
    