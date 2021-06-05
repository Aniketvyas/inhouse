
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.db.models import Subquery
from django.contrib.auth.models import User , auth , Group
import datetime as dt
from .models import *
import random
from django.contrib import messages


def dashboardView(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        dataObj = User.objects.get(username=request.user).groups.all()
        context={}
        for i in dataObj:
            context[str(i.name)]=True
        print(context)
        return render(request,'dashboard.html',context)
    else:
        return redirect('/accounts/login')


def home(request):
    obj = User.objects.get(username=request.user).groups.all()
    print(obj)
    if obj :
        id = obj[0].name
        if id == "DEAN":
            return render(request,'dean/dashboard.html')
        elif id =="COE":
            return render(request,'coe/dashboard.html')
        elif id =="STUDENT":
            data = stud_details.objects.get(UniversityEmailID = request.user)
            return render(request,'student/dashboard.html',{'data':data})
        elif id== "HOD":
            department = Department.objects.get(HeadOfDepartment = employee.objects.get(universityEmail=request.user))
            print(department)
            return render(request,'hod/dashboard.html',{'dept':department})
        elif id=="FACULTY":
            data = faculty.objects.get(FacultyID = employee.objects.get(universityEmail =request.user))
            return render(request,'faculty/dashboard.html',{'data':data})
        elif id=="REGISTRAR":
            return render(request,'registrar/dashboard.html')
        elif id =="VICE-CHANCELLOR":
            return render(request,'vc/dashboard.html')
    else:
        return HttpResponse('BAD Request')
    




#------------------------ MAIN ACADEMICS --------------------------------------------
def Etype(request,id):
    print(id)
    id = employee.objects.filter(employeeID=request.user)
    print(id)
    for i in id:
        id = i.Etype
    print("employee",id)
    if stud_details.objects.filter(UniversityEmailID=request.user).exists():
        return redirect('/socrates')
    elif employee.objects.filter(employeeID = request.user).exists():
        
        if id == "DEANSOE":
            return render(request,'dean/dashboard.html')
        elif id =="DEANSOM":
            return render(request,'dean/dashboard.html')
        elif id =="COE":
            return render(request,'coe/dashboard.html')
        elif id== "HOD":
            return render(request,'hod/dashboard.html')
        elif id=="ASSISTANT-PROF":
            return render(request,'faculty/dashboard.html')
        elif id=="REGISTRAR":
            return render(request,'registrar/dashboard.html')
        elif id == "VICE-CHANCELLOR":
            return render(request,'vc/dashboard.html')
    else:
        return HttpResponse("ERROR 404 File not Found..!!")



def lecture(request):
    print(request.user)
    id = employee.objects.filter(employeeID = request.user)
    for i in id:
        id = i.Department
    print(id)
    students = stud_details.objects.filter(Department=id).count
    faculti = faculty.objects.filter(Department =id).count
    lecture = subjects.objects.filter(Department = id)
    context ={
        'department':department,
        'students' : students,
        'faculty' :faculti,
        'lectures' : lecture,
        'lecture_count' : lecture.count()
    }
    courses = faculty.objects.all().order_by('FieldOfExpertise').distinct()
    print(courses)
    return render(request , 'hod/lecture.html',context)

def studentLectureView(request):
    lectures = lectureEnrollment.objects.filter(student = stud_details.objects.get(UniversityEmailID=request.user))
    return render(request,'student/lecture.html',{'lecture':lectures})


def studentTrackView(request,lecture):
    obj = lectureRecord.objects.filter(lectureId=subjects.objects.get(id=lecture))
    return render(request,'bs4_Horizontal_timeline.html',{'track':obj,'student':True})

def AddLecture(request):
    if request.method=="POST":
        sub = request.POST['SubName']
        sem = request.POST['Sem']
        elig_teacher = request.POST['teacher']
        credit = request.POST['credit']
        branch = request.POST['Branch']
        while True:
            code = branch +"-"+ str(sem)+ str(random.randint(1,99))
            if subjects.objects.filter(LectureID = code).exists():
                continue
            else:
                break
        print(code)
        lec = lectures(LectureID = code,
                LectureName = sub,
                Semester = sem,
                TaughtBy = elig_teacher,
                Credit = credit)
        lec.save()

        return redirect('/academic/hod')

def remove(request):
    if request.method=="POST":
        code = request.POST['code']
        if subjects.objects.filter(LectureID = code).exists():
            subjects.objects.filter(LectureID = code).delete()
            return redirect('/academic/lecture/view')
        else:
            return redirect('/academic/lecture/view')
        
def faculty_info(request):
    faculties = faculty.objects.all()
    return render(request,'dean/department.html',{'faculties':faculties})
    
def deanDepartmentView(request):
    course = Department.objects.filter(School=school.objects.get(dean=employee.objects.get(universityEmail=request.user)))
    print(course)
    return render(request,'dean/department.html',{'courses':course})

def deanDepartmentDetailView(request,id):
    department = Department.objects.filter(DepartmentID = id)
    students = stud_details.objects.filter(Department=id).count
    faculti = faculty.objects.filter(Department =id).count
    lecture = subjects.objects.filter(Department = id)
    context ={
        'department':department,
        'students' : students,
        'faculty' :faculti,
        'lectures' : lecture,
        'lecture_count' : lecture.count()
    }
    return render(request,'dean/lecture.html',context)

    # elif id=="add":
    #     if request.method=="POST":
    #         Deptname = request.POST['DeptName']
    #         DeptID = request.POST['DeptID']
    #         head = request.POST['head']
    #         schoolData = request.POST['School']
    #         if Department.objects.filter(DepartmentID = DeptID ).exists() or Department.objects.filter(DepartmentName=Deptname).exists() or Department.objects.filter(HeadOfDepartment=head).exists():  
    #             messages.info(request,'Invalid Credentials')
    #             return redirect('/academic/department/add')
    #         else:
    #             obj = Department(
    #                 DepartmentName=Deptname , DepartmentID = DeptID , HeadOfDepartment='none' , School=school
    #             , StartDate = dt.datetime.now().date(),
    #             SpecializedCourse=False,Status = False)
    #             obj.save()
    #             subject = 'Assigning new username of hod'
    #             message = 'Hello , we need a new username of the category HOD for the'+ str(Deptname)+' and assign it to the' + (head)+"\nThanks,\n DEAN SOE"
    #             email = EmailMessage(subject, 
    #                 message, EMAIL_HOST_USER, ['aniket.vyas@spsu.ac.in'])
    #             email.fail_silently = False
    #             email.send()
                
    #             print("department can be created")
    #             messages.info(request,'Department Added Successfully')
    #             return redirect('/academic/dean')
    #     heads=faculty.objects.all().order_by('Department')
    #     return render(request,'dean/department.html',{'heads':heads,'addDepartment':True})
    # else:
    #     department = Department.objects.filter(DepartmentID = id)
    #     students = stud_details.objects.filter(Department=id).count
    #     faculti = faculty.objects.filter(Department =id).count
    #     lecture = subjects.objects.filter(Department = id)
       
    #     context ={
    #         'department':department,
    #         'students' : students,
    #         'faculty' :faculti,
    #         'lectures' : lecture,
    #         'lecture_count' : lecture.count(),
    #         'heads': heads
    #     }
    #     return render(request,'dean/department.html',context)

def DepartmentFaculty(request,id):
    return render(request,'dean/department.html',{'faculties':faculty.objects.all()})

#------------------------------ASSISTANT PROFESSORS -----------------------------

def asstlecture(request):
    obj = subjects.objects.filter(TaughtBy=faculty.objects.get(FacultyID = employee.objects.get(universityEmail= request.user)))
    return render(request,'faculty/lecture.html',{'lect':obj,'lecture':True})

def assLectureView(request,lecture):
    lectur = lectureEnrollment.objects.filter(lecture=subjects.objects.get(pk=lecture))
    lects = subjects.objects.filter(pk=lecture)
    context = {
        'outs':lectur,
        'ongoing':lects,
        'assLectureView':True
    }
    if lecture is None:
        context['emptyEnrollment']= True
    
    print(lects,lectur)
    return render(request,'faculty/lecture.html',context)

def lectureRequest(request):
    if request.method == "POST":
        a = request.FILES['lesson']
        b = request.POST['credit']
        c = request.POST['subjectName']
        d = request.POST['semester']
        t = faculty.objects.get(FacultyID=request.user).Department
        print(t)
        id =  random.randint(1,1000)
        filename = fs.save(str(t)+"/"+str(id)+'/'+str(c) , a)
        image_url = fs.url(filename)
        print(image_url)
        lect = TempLectures(
            TempLectureID =id,
            TempLessonPlan = image_url,
            CreatedBy = request.user.username,
            Department = t,
            Semester = d,
            LectureTitle = c,
            LastApprovedBy="PROFESSOR",
            LectureStatus = "UC",
            LastChangesMadeBy = "PROFESSOR",
            NextSendTo = "HOD",
            Changes = "NONE"
        )
        lect.save()
        return redirect('/academic/ASSTPROF/lecture/view')
    else:
        return render(request,'faculty/lecture.html',{'lectureRequest':True})  

    
def lectureStatus(request):
    lect = TempLectures.objects.filter(CreatedBy = request.user.username,NextSendTo='PROFESSOR')
    return render(request,'faculty/lecture.html',{'lect':lect,'lect1':lect,'lectureStatus':True,'trackedLecture':True})

def lectureChangeInfo(request,id):
    if request.method=="POST":
        a = request.FILES['lesson']
        credit = request.POST['credit']
        subject = request.POST['subject']
        sem = request.POST['semester']
        t = faculty.objects.filter(FacultyID=request.user)
        print(t)
        for i in t:
            t = str(i.Department)
        print(t)
        filename = fs.save(t+"/"+str(subject)+"/"+a.name , a)
        image_url = fs.url(filename)
        print(image_url)
        TempLectures.objects.filter(TempLectureID = id).update(
            Credit=credit,
            LectureTitle =subject , 
            TempLessonPlan=image_url,
            Semester = sem,
            LastChangesMadeBy="PROFESSOR",
            NextSendTo="HOD")
        return redirect('/academic/ASSTPROF/lecture/view')



def trackLecture(request,id):
    if request.method == "POST":
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        goals = request.POST['goals']
        notes= request.FILES["notes"]
        if lectureRecord.objects.filter(startDate=startDate,endDate=endDate):
            messages.error(request,'Goals for today already exists')
            return redirect(f'/academic/ASSTPROF/lecture/{id}/Track',id)
        else:
            lectureRecord(startDate=startDate,endDate=endDate,goals=goals,notes=notes,
            subject = subjects.objects.get(pk=id),
            faculty = faculty.objects.get(FacultyID=employee.objects.get(universityEmail =request.user))).save()
            return redirect(f'/academic/ASSTPROF/lecture/{id}/view',id)
    else:
        # print(faculty.objects.filter(FacultyID=request.user),subjects.objects.filter(pk=id))
        obj = lectureRecord.objects.filter(faculty=faculty.objects.get(FacultyID=employee.objects.get(universityEmail=request.user)),subject=subjects.objects.get(pk=id))
        print(obj)
        return render(request,'faculty/lecture.html',{'trackLecture':True,'trackedLecture':True,"track":obj,'prof':True})





#---------------------------------Head Of Department--------------------------------
def hodLecture(request):
    faculties = faculty.objects.filter(Department = Department.objects.get(HeadOfDepartment = employee.objects.get(universityEmail=request.user)))
    lect = subjects.objects.filter(Department = Department.objects.get(HeadOfDepartment = employee.objects.get(universityEmail=request.user)))
    print(lect)
    return render(request,'hod/lecture.html',{'lectureInformation':lect,'lectureInfo':True,'faculties':faculties})



def HodAssignFaculty(request,id):
    if request.method == "POST":
        a = request.POST['faculty']
        faculty1 = faculty.objects.get(id=a)
        # lecture1 = subject.objects.get(id=id)
        print(id)
        subjects.objects.filter(id=id).update(TaughtBy = faculty1)
        return redirect('/academic/HOD/lecture/view')


def HodLectureRequest(request):
    lect = TempLectures.objects.filter(NextSendTo = "HOD")
    return render(request,'hod/lecture.html',{'lect':lect})


def lectureConfigureRequest(request,id):
    user = employee.objects.get(employeeID=request.user).Etype
    if user == "HOD":
        TempLectures.objects.filter(TempLectureID=id).update(NextSendTo="PROFESSOR")
        return redirect('/academic/HOD/lecture/lectureRequest')
    elif user == 'DEANSOE':
        TempLectures.objects.filter(TempLectureID=id).update(NextSendTo="HOD")
        return redirect('/academic/deanEng/lecture/lectureRequest')


# def OngoingLectureView(request):
#     lect = lectures.objects.filter(Department=Department.objects.get(HeadOfDepartment = request.user.username))
#     return render(request,'hod/lectureOngoing.html',{'lectures':lect})


def LectureEnrollments(request):
    data = program.objects.all()
    context = {
        'programs':data,
        'lectureEnroll':True
    }
    return render(request,'hod/lecture.html',context)


def LectureEnrollmentSecond(request,id):
    if request.method == "POST":
        a = request.POST['semester']
        prog = program.objects.get(id=id)
        students = stud_details.objects.filter(program=prog,currentSemester=a)
        subject = subjects.objects.filter(Semester = a,Department = Department.objects.get(HeadOfDepartment = employee.objects.get(universityEmail=request.user)))
        print(subject,students)
        if lectureEnrollment.objects.filter(lecture__in = Subquery(subject.values('id'))).exists():
            context = {
                'data':lectureEnrollment.objects.filter(lecture__in = Subquery(subject.values('id'))),
                "showLectureEnrollment":True
            }
            messages.error(request,'Students are Already Enrolled')
            return render(request,'hod/lecture.html',context)
        for i in students:
            for j in subject:
                d = lectureEnrollment(
                    student = i,
                    lecture = j
                ).save()
                # print(d)
        lect=lectureEnrollment.objects.filter(lecture__in = Subquery(subject.values('id')))
        print(lect)
        context = {
            'data':lect,
            'showLectureEnrollment':True
        }
        return render(request,'hod/lecture.html',context)


def LectureEnrollmentDone(request,LectureID,EnrollmentNumber):
    data = stud_details.objects.get(EnrollmentNumber = EnrollmentNumber)
    lect = subjects.objects.get(id = LectureID)
    lectureEnrollment(
        student = data,
        lecture = lect
    ).save()
    return redirect('/academic/HOD/lecture/'+str(LectureID)+'/Enrollment')



# def lectureFilter(request , id):
#     if request.method == "POST":
#         sem = int(request.POST['sem'])
#         l = stud_details.objects.filter(CurrSem=sem,Department = Department.objects.get(HeadOfDepartment=employee.objects.get(universityEmail=request.user))).exclude(id__in = Subquery(lectureEnrollment.objects.filter(lectureId=subjects.objects.get(id=id)).values('studentID')))
#         print(l)
#         return render(request, 'hod/lecture.html',{'student':l,'lectureEnroll':True})


def lol(request,lecture):
    lectur = lectureEnrollment.objects.filter(lecture=subjects.objects.get(id=lecture))
    lects = subjects.objects.filter(id=lecture)
    return render(request,'hod/lecture.html',{'outs':lectur,'ongoing':lects})

def trackLectureHod(request,id):
    obj = lectureRecord.objects.filter(lectureId=subjects.objects.get(id=id))
    return render(request,'bs4_Horizontal_timeline.html',{'track': obj,'hod':True })





def OutpassRequests(request):
    #ik@123
    #p = stud_outing.objects.raw('select "Department_id" from academics_stud_details as sd , outpass_stud_outing as so where sd."EnrollmentNumber" = so."EnrollmentNumber" ;')
    e = Department.objects.get(HeadOfDepartment=request.user.username).DepartmentID
    print(e)
    a = stud_outing.objects.filter(EnrollmentNumber__in=Subquery(stud_details.objects.filter(Department=e).values('EnrollmentNumber')),Req_status='Forwaded')
    return render(request,'hod/outpass.html',{'out':a})

    
#-------------------------DEAN OF ENGINEERING ------------------------------------------

def deanLecture(request):
    return render(request,'dean/lecture.html')

def DeanLectureRequest(request):
    lect = TempLectures.objects.filter(NextSendTo = "DEAN")
    return render(request,'dean/lecture.html',{'lect':lect})

def DeanOngoingRequest(request):
    lect = subjects.objects.all()
    return render(request,'dean/lecture.html',{'lect':lect})
    
def lectureChangeRequest(request,id):
    print(id)
    asl = id
    if request.method=="POST":
        content = request.POST['Changes']
        branch = TempLectures.objects.filter(TempLectureID=id)
        for i in branch:
            Department = i.Department
            subject = i.LectureTitle
            change = i.Changes
            fil = i.TempLectureID
            subject = i.LectureTitle
        print(Department,content)
        if change == 'NONE':
            document = Document()
            print(request.user.get_full_name)
            document.add_heading('\tChanges Suggested By '+str(request.user.get_full_name())+' on'+str(dt.datetime.now().date())+'\t')
            document.add_paragraph(content)
            document.save('media/'+str(Department)+"/"+str(asl)+"/"+str(id)+'.docx')
            change='media/'+str(Department)+"/"+str(asl)+"/"+str(id)+'.docx'
        else:
            print("change",change)
            document = Document('media'+"/"+str(Department)+"/"+str(asl)+"/"+str(id)+'.docx')
            print('docuemet created')
            print(request.user.get_full_name)
            document.add_heading('\tChanges Suggested By '+str(request.user.get_full_name())+'\t')
            document.add_paragraph(content)
            print(change)
            document.save('media'+"/"+str(Department)+"/"+str(asl)+"/"+str(id)+'.docx')
        print("File created Successfully")

        TempLectures.objects.filter(TempLectureID=id).update(Changes=change)
        id = employee.objects.filter(employeeID=request.user)
        for i in id:
            id = i.Etype
        print(id)
        if id=='HOD':
            a=TempLectures.objects.filter(TempLectureID=asl)
            for i in a:
                print(i.LastChangesMadeBy,i.NextSendTo)
            TempLectures.objects.filter(TempLectureID=asl).update(LastChangesMadeBy='HOD',NextSendTo='PROFESSOR')
            a=TempLectures.objects.filter(TempLectureID=asl)
            for i in a:
                print(i.LastChangesMadeBy,i.NextSendTo)
            lect = TempLectures.objects.filter(LectureStatus='UC',NextSendTo='HOD')
            return redirect('/academic/HOD/lecture/lectureRequest',{'lect':lect})
        elif id == "DEANSOE":
            TempLectures.objects.filter(TempLectureID=asl).update(LastChangesMadeBy='DEAN',NextSendTo='HOD')
            lect = TempLectures.objects.filter(LectureStatus='UC',NextSendTo='DEAN')
            return redirect('/academic/deanEng/lecture/lectureRequest',{'lect':lect})

        elif id == "VICE-CHANCELLOR":
            TempLectures.objects.filter(TempLectureID=asl).update(LastChangesMadeBy='VC',NextSendTo='DEAN')
            lect = TempLectures.objects.filter(LectureStatus='UC',NextSendTo='VC')
            return redirect('/academic/vc/lecture/lectureRequest',{'lect':lect})

        

def lectureApproveRequest(request,id):
    user = request.user
    userType = employee.objects.filter(employeeID=user)
    for i in userType:
        userType = i.Etype
        de = i.Department
    print(userType)
    if userType=="HOD":
        lect = TempLectures.objects.filter(Department=de)
        TempLectures.objects.filter(TempLectureID=id).update(LastApprovedBy='HOD',NextSendTo='DEAN')
        return redirect('/academic/HOD/lecture/lectureRequest',{'lect':lect})
    elif userType=="DEANSOE":
        lect = TempLectures.objects.filter(Department=de)
        TempLectures.objects.filter(TempLectureID=id).update(LastApprovedBy='DEAN',NextSendTo="VC")
        return redirect('/academic/deanEng/lecture/lectureRequest',{'lect':lect})



#-------------------------- VICE - CHANCELLOR ----------------------------------
def lectureView(request):
    department = Department.objects.all().count
    students = stud_details.objects.all().count
    faculti = faculty.objects.all().count
    lecture = subjects.objects.all()
    context ={
            'department':department,
            'students' : students,
            'faculty' :faculti,
            'lectures' : lecture,
            'lecture_count' : lecture.count()
    }
    return render(request,'vc/lectures.html',context)


def vclectureRequest(request): 
    lect = TempLectures.objects.filter(NextSendTo="VC")
    return render(request,'vc/lectureStatus.html',{'lect':lect})


def lectureApproveVc(request,id):
    temp = TempLectures.objects.get(TempLectureID=id)
    while True:
        id = random.randint(10000,999999)
        if subjects.objects.filter(id=id).exists():
            continue
        else:
            break
    lect = lectures(
        id = id,
        LectureID = temp.TempLectureID,
        LectureName = temp.LectureTitle,
        LessonPlan = temp.TempLessonPlan,
        TaughtBy = faculty.objects.get(FacultyID = temp.CreatedBy),
        Credit = temp.Credit,
        LastTaughtBy = "No",
        Department = temp.Department,
        Semester = temp.Semester
    )
    lect.save();
    temp.delete()
    return redirect('/academic/vc')






# -------------------------------- QUIZ ----------------------------

def quizHost(request):
    if request.method == "POST":
        name = request.POST['quizName']
        subject = subjects.objects.get(id = request.POST['subject'])
        dateQuiz = request.POST['quizDate']
        startTime = request.POST['startTime']
        endTime = request.POST['endTime']
        if quizInfo.objects.filter(name=name,subject=subject,quizDate=dateQuiz,quizEndTime=endTime,quizStartTime=startTime).exists():
            context = {
                'inputQuizInfo': True,
                'subjects' : subjects.objects.filter(TaughtBy=faculty.objects.get(FacultyID = employee.objects.get(universityEmail= request.user)))
            }
            messages.error(request,'Quiz with this credentials already exists..!!')
            return render(request,'faculty/quiz.html',context)

        else:
            quizObj = quizInfo(
                name=name,
                subject=subject,
                quizDate=dateQuiz,
                quizEndTime=endTime,
                quizStartTime=startTime)
            quizObj.save()
            context = {
                'quizObj' : quizObj,
                'inputQuestions': True
            }
            messages.success(request,'Quiz created Successfully, Please Add Questions to it..!')
            return redirect('/academic/ASSTPROF/lecture/quiz/'+str(quizObj.id)+'/enterQuestions/view')

    context = {
        'inputQuizInfo':True,
        'subjects':subjects.objects.filter(TaughtBy=faculty.objects.get(FacultyID = employee.objects.get(universityEmail= request.user)))
    }
    return render(request,'faculty/quiz.html',context)


def enterQuestions(request,id,questionType):
    if request.method == "POST":
        quizObj = quizInfo.objects.get(id=id)
        quizQuestionsData = quizQuestions.objects.filter(quiz= quizObj)
        if questionType == "mcq":
            a = request.POST['question']
            print("E",a)
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            correctOption = request.POST['correctAnswer']
            if quizQuestions.objects.filter(question=a).exists():
                messages.error(request,'This question already exists')
                context = {
                    'quizQuestions': quizQuestions.objects.filter(quiz= quizObj),
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                print(quizQuestions.objects.filter(quiz= quizObj))
                return redirect('/academic/ASSTPROF/lecture/quiz/'+str(id)+'/enterQuestions',context)
            else:
                # quiz= quizInfo.objects.get(id =id)
                quizQuestions(
                    question = a,
                    questionType = 'MCQ',
                    quiz=quizObj,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correctOption=correctOption,
                ).save()

                
                print(quizQuestionsData)
                context = {
                    'quizQuestions':quizQuestionsData,
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                messages.info(request,'Added Successfully.!')
                return redirect('/academic/ASSTPROF/lecture/quiz/'+str(quizObj.id)+'/enterQuestions/view',context)
        else:
            question = request.POST['questionn']
            answer  = request.POST['natAnswer']
            if quizQuestions.objects.filter(question=question).exists():
                messages.error(request,'This question already exists')
                a = "ASSTPROF/lecture/quiz/<str:id>/enterQuestions/<str:questionType>"
                print(quizQuestions.objects.filter(quiz= quizObj))
                context = {
                    'quizQuestions':quizQuestionsData,
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                return redirect('/academic/ASSTPROF/lecture/quiz/'+str(id)+'/enterQuestions/'+'view',context)
            else:
                quizQuestions(
                        question = question,
                        questionType = 'typenat',
                        quiz=quizObj,
                        correctOption=answer,
                    ).save()
                messages.info(request,'Added Successfully.!')
                context = {
                    'quizQuestions':quizQuestionsData,
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                return redirect('/academic/ASSTPROF/lecture/quiz/'+str(id)+'/enterQuestions/'+'view',context)
    else:
        quizObj= quizInfo.objects.get(id =id)
        quizQuestionsData = quizQuestions.objects.filter(quiz=quizInfo.objects.get(id=id))
        print(quizQuestionsData)
        context = {
             'quizQuestions':quizQuestionsData,
                    'quizObj' : quizObj,
                    'inputQuestions': True
                }
        return render(request,'faculty/quiz.html',context)

def previousQuizDetails(request,id,command,questionType):
    if command == "ViewDetails":
        quiz = quizInfo.objects.get(id=id)
        quizQuestionsData = quizQuestions.objects.filter(quiz=quiz)
        context={
            'previousQuizDetailsView':True,
            'quizInfo':quiz,
            'quizQuestionData':quizQuestionsData
        } 
        return render(request,'faculty/quiz.html',context)
    elif command == "addQuestions":
        quizObj = quizInfo.objects.get(id=id)
        quizQuestionsData = quizQuestions.objects.filter(quiz= quizObj)
        if questionType == "mcq":
            a = request.POST['question']
            print("E",a)
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            correctOption = request.POST['correctAnswer']
            if quizQuestions.objects.filter(question=a).exists():
                messages.error(request,'This question already exists')
                context = {
                    'quizQuestions': quizQuestions.objects.filter(quiz= quizObj),
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                print()
                return redirect('/academic/ASSTPROF/lecture/previousQuiz/'+str(id)+'/ViewDetails/show',context)
            else:
                # quiz= quizInfo.objects.get(id =id)
                quizQuestions(
                    question = a,
                    questionType = 'MCQ',
                    quiz=quizObj,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correctOption=correctOption,
                ).save()

                
                # print(quizQuestionsData)
                context = {
                    'quizQuestions':quizQuestionsData,
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                messages.info(request,'Added Successfully.!')
                return redirect('/academic/ASSTPROF/lecture/previousQuiz/'+str(id)+'/ViewDetails/show',context)
        else:
            question = request.POST['questionn']
            answer  = request.POST['natAnswer']
            if quizQuestions.objects.filter(question=question).exists():
                messages.error(request,'This question already exists')
                a = "ASSTPROF/lecture/quiz/<str:id>/enterQuestions/<str:questionType>"
                print(quizQuestions.objects.filter(quiz= quizObj))
                context = {
                    'quizQuestions':quizQuestionsData,
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                return redirect('/academic/ASSTPROF/lecture/previousQuiz/'+str(id)+'/ViewDetails/show',context)
            else:
                quizQuestions(
                        question = question,
                        questionType = 'typenat',
                        quiz=quizObj,
                        correctOption=answer,
                    ).save()
                messages.info(request,'Added Successfully.!')
                context = {
                    'quizQuestions':quizQuestionsData,
                    'inputQuestions' : True,
                    'quizObj': quizObj
                }
                return redirect('/academic/ASSTPROF/lecture/previousQuiz/'+str(id)+'/ViewDetails/show',context)


def deleteQuestions(request,quizId,questionId):
    quizQuestions.objects.filter(id=questionId).delete()
    print("blah")
    messages.info(request,'Question Deleted Successfully.!')
    
    return redirect('/academic/ASSTPROF/lecture/previousQuiz/'+str(quizId)+'/ViewDetails/show')

def updateQuestions(request,id,questionType,questionId):
    if request.method == "POST":
        if questionType == 'mcq':
            a = request.POST['question']
            questionId = request.POST['questionID']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            correctOption = request.POST['correctAnswer']
            questionObj = quizQuestions.objects.filter(id=questionId)
            questionObj.update(question=a,option1=option1,option2=option2,option3=option3,option4=option4,correctOption=correctOption)
            return redirect('/academic/ASSTPROF/lecture/previousQuiz/'+str(questionObj[0].quiz.id)+'/ViewDetails/show')
        elif questionType == 'nat':
            a = request.POST['questionn']
            questionId = request.POST['questionID']
            correctOption = request.POST['natAnswer']
            questionObj = quizQuestions.objects.filter(id=questionId)
            questionObj.update(question=a,correctOption=correctOption)
            return redirect('/academic/ASSTPROF/lecture/previousQuiz/'+str(questionObj[0].quiz.id)+'/ViewDetails/show')
        else:
            return HttpResponseBadRequest('Authorization Bypassed Turning off!!')
    else:
        return HttpResponseBadRequest()


def previousQuiz(request):
    quizObj = quizInfo.objects.filter(subject__in = Subquery(subjects.objects.filter(TaughtBy=faculty.objects.get(FacultyID = employee.objects.get(universityEmail= request.user))).values('id')))
    context = {
        'quizData':quizObj,
        'previousQuiz':True
    }
    return render(request,'faculty/quiz.html',context)



# ------------------------------- Assignments --------------------------------------


def createAssignments(request):
    if request.method == "POST":
        # name = request.POST['']
        subject = request.POST['subject']
        assignmentName = request.POST['assignmentName']
        assignmentFil = request.FILES['assignmentFile']
        deadline = request.POST['endTime']
        assignmentDate = request.POST['assignmentDate']
        assignment(
            subject = subjects.objects.get(id= subject),
            name = assignmentName,
            assignmentFile = assignmentFil,
            deadline = deadline,
            startingDate = assignmentDate
        ).save()
        return redirect('/academic/ASSTPROF/lecture/previousAssignments')
    else:
        context = {
            'facultyAssignmentCreationView':True,
            'subjectsInfo' : subjects.objects.filter(TaughtBy=faculty.objects.get(FacultyID = employee.objects.get(universityEmail= request.user))),
        }
        return render(request,'faculty/assignment.html',context)

def previousAssignment(request):
    context = {
        'assignmentData':assignment.objects.filter(subject__in = Subquery(subjects.objects.filter(TaughtBy=faculty.objects.get(FacultyID = employee.objects.get(universityEmail= request.user))).values('id'))),
        'facultyPreviousAssignmentView':True,
        'subjectsInfo' : subjects.objects.filter(TaughtBy=faculty.objects.get(FacultyID = employee.objects.get(universityEmail= request.user))),
        
    }
    return render(request,'faculty/assignment.html',context)

def updatePreviousAssignment(request,id):
    if request.method == "POST":
        subject = request.POST['subject']
        assignmentName = request.POST['assignmentName']
        assignmentFil = request.FILES['assignmentFile']
        deadline = request.POST['endTime']
        assignmentDate = request.POST['assignmentDate']
        assignment.objects.filter(id=id).update(
            subject = subjects.objects.get(id= subject),
            name = assignmentName,
            assignmentFile = assignmentFil,
            deadline = deadline,
            startingDate = assignmentDate
        )
        return redirect('/academic/ASSTPROF/lecture/previousAssignments')

def deletePreviousAssignment(request,id):
    assignment.objects.get(id=id).delete()  
    return redirect('/academic/ASSTPROF/lecture/previousAssignments')


def quizStudentView(request):
    context={
        'quizObject':True
    }
    return render(request,'student/quiz.html',context)

def assignmentStudentView(request):
    mainList=[]
    assignmentObject = assignment.objects.filter(subject__in = Subquery(lectureEnrollment.objects.filter(student=stud_details.objects.get(UniversityEmailID=request.user)).values('lecture')))
    for i in assignmentObject:
        objectData = assignmentSubmission.objects.filter(assignment=i,submitedBy = stud_details.objects.get(UniversityEmailID=request.user)).first()
        if objectData :
            dataDictionary = {
                'alreadySubmitted':True,
                'submissionsQuerySet':objectData,
                'querySetObject':i
            }
        else:
            dataDictionary= {
                'alreadySubmitted':False,
                'submissionsQuerySet':objectData,
                'querySetObject':i
            }
        mainList.append(dataDictionary)
    print(assignmentObject)
    print(mainList)
    context = {
        'assignmentData':mainList,
        'studentPreviousAssignmentView':True
    }
    return render(request,'student/assignment.html',context)


'''
class assignmentSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey('assignment',on_delete=models.CASCADE)
    submissionFile = models.FileField()
    submitedBy = models.ForeignKey('stud_details',on_delete=models.CASCADE)
    submitedOn = models.DateTimeField(auto_now_add=True)

'''

def studentAssignmentSubmitView(request,id):
    if request.method=="POST":
        file = request.FILES['assignmentSubmitedFile']
        assignmentSubmission(
            assignment=assignment.objects.get(id=id),
            submissionFile =file,
            submitedBy = stud_details.objects.get(UniversityEmailID = request.user)
        ).save()
        return redirect('/academic/student/assignmentStudentView')

    
def studentUpdateAssignmentView(request,id):
    if request.method == "POST":
        file = request.FILES['assignmentUpdatedFile']
        assignmentSubmission.objects.filter(assignment=assignment.objects.get(id=id),submitedBy=stud_details.objects.get(UniversityEmailID=request.user)).update(submissionFile = file)
        print(assignmentSubmission.objects.get(assignment=assignment.objects.get(id=id),submitedBy=stud_details.objects.get(UniversityEmailID=request.user)).submissionFile)
        return redirect('/academic/student/assignmentStudentView')

def facultyAssignmentSubmissionView(request,id):
    dataPacket = assignmentSubmission.objects.filter(assignment=assignment.objects.get(id=id))
    context = {
        'dataPacket':dataPacket,
        'facultyAssignmentSubmissionView' :True
    }
    return render(request,'faculty/assignment.html',context)