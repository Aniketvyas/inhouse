from django.shortcuts import render
# from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Subquery
import datetime as dt
from django.core.files.storage import FileSystemStorage
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
        Department(
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
    Department.objects.filter(id=id).delete()
    return Response({'result':'success'},status=200)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def update_hod(request,id):
    if request.method=='GET':
        qs = Department.objects.filter(id=id)
        serializer = departmentSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        print(request.data['HeadOfDepartment'])
        Department.objects.filter(id=id).update(HeadOfDepartment=employee.objects.get(Email = request.data['HeadOfDepartment']))
        return Response({'result':'Updation Successfull'},status=200)





@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def lecture(request,id):
    if request.method=='GET':
        qs = subjects.objects.all()
        serializer = subjectsSerializer(qs,many=True)
        return Response(serializer.data,status=200)
    elif request.method=="POST":
        parser_classes = (JSONParser, FormParser, MultiPartParser)
        #create a lecture request view
        print(request.data)
        serializer = subjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.errors)
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_lecture(request,id):
    subjects.objects.filter(id=id).delete()
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


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def studentQuizInfo(request,id):
    a = quizInfo.objects.filter(
        subject__in = Subquery(
            lectureEnrollment.objects.filter(
                student=stud_details.objects.get(id=id)
                ).values('lecture')
                )
            ).order_by('-quizDate')
    print(a)
    dataPacket = {}
    count=0
    for i in a:
        if quizGrades.objects.filter(quiz=i,student=stud_details.objects.get(id=id)):
            dataPacket[count] = {
                "attempted":True,
                "quizData":quizInfoSerializer(i,many=False).data
            }
        else:
            dataPacket[count] = {
                "attempted":False,
                "quizData":quizInfoSerializer(i,many=False).data
            }
        count+=1
    return Response(dataPacket,status=200)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def studentGetQuestions(request,id):
    quiz = quizInfo.objects.get(id=id)
    if (quiz.quizStartTime <= dt.datetime.now().time()) and (quiz.quizDate <= dt.datetime.now().date()) and (quiz.quizEndTime >= dt.datetime.now().time()):
        q = quizQuestions.objects.filter(quiz=quiz)
        serializer = quizQuestionsSerializer(q,many=True)
        return Response(serializer.data,status=200)
    else:
        return Response({"message":"Forbidden"},status=403)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def submitGrades(request):
    if request.method == "POST":
        quizid = request.data['quizid']
        studentid = request.data['studentid']
        # marks = request.data['marks']
        unAttempted = int(request.data['unAttemptedQuestions'])
        # wrongAnswers = request.data['wrongAnswers']
        correctAnswers = int(request.data['correctAnswers'])
        timeTaken = request.data['timeTaken']
        startedOn1 = request.data['startedOn']
        quiz = quizInfo.objects.get(id=quizid)
        total = quizQuestions.objects.filter(quiz=quiz).count()
        if quizGrades.objects.filter(student = stud_details.objects.get(id=studentid),quiz=quiz).exists():
            context = {
                'error':'Grade Already Exists'
            }
            return Response(context,status=200)
        else:
            quizGrades(
                quiz = quiz,
                student = stud_details.objects.get(id=studentid),
                marks = correctAnswers,
                unAttemptedQuestions = total - unAttempted,
                wrongAnswers = unAttempted - correctAnswers,
                correctAnswers = correctAnswers,
                timeTaken = timeTaken,
                # startedOn = startedOn1
            ).save()
            return Response({"message":"Success"},status=200)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def studentAssignmentView(request,id):
    assignmentObject = assignment.objects.filter(subject__in = Subquery(lectureEnrollment.objects.filter(student=stud_details.objects.get(id=id)).values('lecture')))
    serializer = assignmentSerializer(assignmentObject,many=True)
    return Response(serializer.data,status=200)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def studentAssignmentSubmission(request):
    if request.method == "POST":
        file = request.data['assignmentSubmitedFile']
        if(file):
            # print("not nul")
            print(file)
        # data=base64.b64decode(file)
        assignmentID = request.data['assignmentID']
        studentID = request.data['studentID']
        assignmentSubmission(
            assignment=assignment.objects.get(id=assignmentID),
            submissionFile =file,
            submitedBy = stud_details.objects.get(id=studentID)
        ).save()
        return Response({"Message":"Success"},status=200)
# except :
#         print("Error Occured!")
#         return Response({"Message": "Gand mar gayi code ki!!"},status=200)


