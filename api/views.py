from django.shortcuts import render
# from django.http import HttpResponse
from django.http import JsonResponse 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    qs = stud_details.objects.all()
    if not qs.exists():
        return Response({}, status=404)
    serializer = stud_detailsSerializer(qs,many=True)
    return Response(serializer.data, status=200)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def schoolView(request):
    if request.method=='GET':
        qs = school.objects.all()
        serializer = schoolSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        school(
            name=request.data['name'],
            status=True,
            dean = employee.objects.get(id=request.data['dean'])
        ).save()
        return Response({'result':'save successffull'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_school(request,id):
    school.objects.filter(id=id).delete()
    return Response({'result':"success"},status=200)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def update_dean(request,id):
    if request.method=='GET':
        qs = school.objects.all()
        serializer = schoolSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        pass


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def programView(request,id):
    if request.method=='GET':
        qs = program.objects.all()
        serializer = programSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        program(
        name = request.data['name'],
        school = school.objects.get(id=request.data['school']),
        status = request.data['status']
        ).save()
        return Response({'result':'success'},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_program(request,id):
    program.objects.filter(id=id).delete()
    return Response({'result':'success'},status=200)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def departmentView(request,id):
    if request.method=='GET':
        qs = Department.objects.all()
        serializer = departmentSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        department(
            DepartmentID = request.data['DepartmentID'],
            DepartmentName = request.data['DepartmentName'],
            HeadOfDepartment = employee.objects.get(id=request.data['HeadOfDepartment']),
            SpecializedCourse = request.data['SpecializedCourse'],
            Program = program.objects.get(id=id),
            Status = request.data['Status'] 
        ).save()
        return Response({'result':'success'},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_department(request,id):
    department.objects.filter(id=id).delete()
    return Response({'result':'success'},status=200)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def update_hod(request,id):
    if request.method=='GET':
        qs = department.objects.filter(id=id)
        serializer = departmentSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        print(request.data['HeadOfDepartment'])
        department.objects.filter(id=id).update(HeadOfDepartment=employee.objects.get(Email = request.data['HeadOfDepartment']))
        return Response({'result':'Updation Successfull'},status=200)
        




@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def lecture(request,id):
    if request.method=='GET':
        qs = lectures.objects.all()
        serializer = lecturesSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=="POST":
        parser_classes = (JSONParser, FormParser, MultiPartParser)
        #create a lecture request view
        print(request.data)
        serializer = lecturesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.errors)
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_lecture(request,id):
    lectures.objects.filter(id=id).delete()
    return Response({'result':'sucess'},status=200)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def update_faculty(request,id):
    if request.method=='GET':
        qs= faculty.objects.all()
        serializer = facultySerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        pass

def student(request):
    if request.method=='GET':
        pass
    elif request.method=='POST':
        pass

def delete_student(request,id):
    pass