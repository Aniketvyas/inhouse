
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.db.models import Subquery
from django.contrib.auth.models import User , auth , Group
import datetime as dt
from .models import *
import random
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


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
            department = Department.objects.all()
            context={
                'departmentPacket':department
            }
            return render(request,'coe/dashboard.html',context)
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
    obj = lectureRecord.objects.filter(subject=subjects.objects.get(id=lecture))
    return render(request,'student/lecture.html',{'track':obj,'isTrack':True,'student':True})

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
        obj = lectureRecord.objects.filter(subject=subjects.objects.get(pk=id))
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


# def LectureEnrollmentDone(request,LectureID,EnrollmentNumber):
#     data = stud_details.objects.get(EnrollmentNumber = EnrollmentNumber)
#     lect = subjects.objects.get(id = LectureID)
#     lectureEnrollment(
#         student = data,
#         lecture = lect
#     ).save()
#     return redirect('/academic/HOD/lecture/'+str(LectureID)+'/Enrollment')



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
    obj = lectureRecord.objects.filter(subject=subjects.objects.get(id=id))
    return render(request,'hod/lecture.html',{'track': obj,'hod':True,'trackLecture':True})

def createLecture(request):
    if request.method == "POST":
        subjectName = request.POST['subjectName']
        # subjectCode = request.POST['subjectCode']
        lessonPlan = request.FILES['lessonPlan']
        semester = request.POST['semester']
        facultyr = request.POST['faculty']
        credit = request.POST['credit']
        if subjects.objects.filter(subjectName=subjectName).exists():
            messages.info(request,'Already Exists. !!')
            return redirect('/academic/HOD/lecture/view')
        else:
            department = Department.objects.get(HeadOfDepartment = employee.objects.get(universityEmail= request.user))
            subjectsObject = subjects.objects.filter(Department= department)
            i=0
            while (i<=10):
                subjectCode = str(department.DepartmentID) + "-"+ str(random.randint(int(semester)*1000, ((int(semester)+1)*1000)-1))
                if subjectsObject.filter(subjectCode=subjectCode).exists():
                    continue
                else:
                    break
                i+=1

            subjects(
                subjectName = subjectName,
                subjectCode = subjectCode,
                LessonPlan = lessonPlan,
                TaughtBy = faculty.objects.get(id=facultyr),
                Credit = credit,
                Department=department,
                Semester = semester

            ).save()
            messages.info(request,'Subject Added SuccessFully. !!')
            return redirect('/academic/HOD/lecture/view')






# def OutpassRequests(request):
#     #ik@123
#     #p = stud_outing.objects.raw('select "Department_id" from academics_stud_details as sd , outpass_stud_outing as so where sd."EnrollmentNumber" = so."EnrollmentNumber" ;')
#     e = Department.objects.get(HeadOfDepartment=request.user.username).DepartmentID
#     print(e)
#     a = stud_outing.objects.filter(EnrollmentNumber__in=Subquery(stud_details.objects.filter(Department=e).values('EnrollmentNumber')),Req_status='Forwaded')
#     return render(request,'hod/outpass.html',{'out':a})


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
        duration = request.POST['duration']
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
                quizStartTime=startTime,
                duration=duration)
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
        quizPacket = quizGrades.objects.filter(quiz=quiz)
        dataPacket = []
        context={
            'previousQuizDetailsView':True,
            'quizInfo':quiz,
            'quizQuestionData':quizQuestionsData,
            'quizEvaluationPacket':quizPacket
        }
        print(quiz.quizDate<dt.datetime.now().date())
        if quiz.quizDate < dt.datetime.now().date():
            context['editabel'] = False
        else:
            context['editable'] = True

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
    quizObj = quizInfo.objects.filter(
        subject__in = Subquery(
            subjects.objects.filter(
                TaughtBy=faculty.objects.get(
                    FacultyID = employee.objects.get(
                        universityEmail= request.user)
                        )
                    ).values('id')
                )
            )
    print(quizObj)

    context = {
        'quizData':quizObj,
        'previousQuiz':True
    }
    return render(request,'faculty/quiz.html',context)



def quizStudentView(request):
    quizObject = quizInfo.objects.filter(subject__in = Subquery(lectureEnrollment.objects.filter(student=stud_details.objects.get(UniversityEmailID=request.user)).values('lecture'))).order_by('-quizDate')
    mainList=[]
    for i in quizObject:
        time = i.quizStartTime;
        dataDictionary = {}
        # print(time,dt.datetime.now().time(),i.quizEndTime,time <= dt.datetime.now().time() ,time <= i.quizEndTime)
        if quizGrades.objects.filter(quiz=i,student=stud_details.objects.get(UniversityEmailID=request.user)).exists():
            dataDictionary['isAttemptable'] = False
        else:
            if time <= dt.datetime.now().time() and dt.datetime.now().time() <= i.quizEndTime:
                dataDictionary["isAttemptable"] = True 
            else:
                dataDictionary["isAttemptable"] = False
        dataDictionary['object'] = i
        mainList.append(dataDictionary)
    print(mainList)

    context={
        'quizObject':mainList,
        'result' :False,
        'quizListView':True
    }
    return render(request,'student/quiz.html',context)

def quizDetailView(request,id):
    print(id)
    quizObject = quizInfo.objects.get(id=id)
    quizGradesObject = quizGrades.objects.filter(quiz=quizObject,student = stud_details.objects.get(UniversityEmailID=request.user.username)).first()
    if quizGradesObject:
        context = {
            'quizGradesObject':quizGradesObject,
            'quizResultView':True,
            'totalPercent':quizGradesObject.marks*10,

        }
    else:
         context = {
            'quizResultView':True,
            'signal' : True
        }
    print(context)
    return render(request,'student/quiz.html',context)



def studentAttemptQuiz(request,id):
    quiz=quizInfo.objects.get(id=id)
    print(quiz.quizStartTime <= dt.datetime.now().time() , dt.datetime.now().time() <= quiz.quizEndTime)
    if(quizGrades.objects.filter(quiz=quiz,student=stud_details.objects.get(UniversityEmailID = request.user))).exists():
        if quiz.quizStartTime <= dt.datetime.now().time() and dt.datetime.now().time() <= quiz.quizEndTime:
            object = quizQuestions.objects.filter(quiz=quiz)
            context={
                "attemptQuizStudentView":True,
                "questionsObject":object,
                'quizObject':quiz
            }
            return render(request,'student/quiz.html',context)
        else:
            messages.info(request,'Quiz is not yet started!')
            return render(request,'student/quiz.html')
    else:
        messages.info(request,"you cannot attempt this quiz")
        return render(request,'student/quiz.html')


def studentSubmitQuiz(request,id):
    keys = request.POST.keys()
    correctAnswerCount=0
    print(id)
    inCorrectAnswer =0
    formWalaAnswer =0
    print(keys)
    for i in keys:
        # print(i.split('%'))
        arr=i.split('%')
        print(arr)
        if arr[0] == 'csrfmiddlewaretoken':
            continue 
        else:
            question = quizQuestions.objects.get(id=arr[0])
            correctAnswer = question.correctOption
            if len(arr)==2:
                print(arr[1])
                option = arr[1]
                if option=="option1":
                    formWalaAnswer = question.option1
                elif option == "option2":
                    formWalaAnswer = question.option2
                elif option == "option3":
                    formWalaAnswer = question.option3
                elif option == "option4":
                    formWalaAnswer = question.option4

            else:
                formWalaAnswer = request.POST[i]
            if(formWalaAnswer == correctAnswer):
                print(formWalaAnswer,correctAnswer)
                correctAnswerCount+=1
            elif formWalaAnswer == "":
                continue
            else:
                print(formWalaAnswer,correctAnswer,'in')
                inCorrectAnswer+=1

    print(quizQuestions.objects.filter(quiz=quizInfo.objects.get(id=id)).count(),inCorrectAnswer+correctAnswerCount)
    print("incorrect",inCorrectAnswer,"correct",correctAnswerCount)
      
    quizGrades(
        quiz = quizInfo.objects.get(id=id),
        student = stud_details.objects.get(UniversityEmailID = request.user),
        unAttemptedQuestions = quizQuestions.objects.filter(quiz=quizInfo.objects.get(id=id)).count()-(inCorrectAnswer+correctAnswerCount),
        wrongAnswers = inCorrectAnswer,
        correctAnswers = correctAnswerCount,
        timeTaken = "10",
        marks = correctAnswerCount
    ).save()
    return redirect('/academic/student/'+str(id)+'/quizDetailView')
      


    # print(quizQuestions.objects.filter(quiz=quizInfo.objects.get(id=id)))
    # context={}
    # return render(request,'student/quiz.html',context)

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



def assignmentStudentView(request):
    mainList=[]
    # print(request.user)
    assignmentObject = assignment.objects.filter(subject__in = Subquery(lectureEnrollment.objects.filter(student=stud_details.objects.get(UniversityEmailID=request.user)).values('lecture')))
    for i in assignmentObject:
        # print(i)
        objectData = assignmentSubmission.objects.filter(assignment=i,submitedBy = stud_details.objects.get(UniversityEmailID=request.user))
        # print(objectData[0].submitedBy, objectData[0].assignment,i)
        if objectData :
            dataDictionary = {
                'alreadySubmitted':True,
                'submissionsQuerySet':objectData[0],
                'querySetObject':i
            }
        else:
            dataDictionary= {
                'alreadySubmitted':False,
                'submissionsQuerySet':objectData,
                'querySetObject':i
            }
        mainList.append(dataDictionary)
    # print(assignmentObject)
    # print(mainList)
    context = {
        'assignmentData':mainList,
        'studentPreviousAssignmentView':True
    }
    print(mainList)
    return render(request,'student/assignment.html',context)


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
        print(request.FILES)
        
        file = request.FILES['assignmentUpdatedFile']
        fs = FileSystemStorage()
        file = fs.save(file.name,file)
        print(id,file,assignmentSubmission.objects.get(id=id))
        assignmentSubmission.objects.filter(id=id).update(submissionFile = file)
        # print(assignmentSubmission.objects.get(assignment=assignment.objects.get(id=id),submitedBy=stud_details.objects.get(UniversityEmailID=request.user)))
        messages.info(request,'updated Sucessfully!')
        return redirect('/academic/student/assignmentStudentView')

def facultyAssignmentSubmissionView(request,id):
    dataPacket = assignmentSubmission.objects.filter(assignment=assignment.objects.get(id=id))
    context = {
        'dataPacket':dataPacket,
        'facultyAssignmentSubmissionView' :True
    }
    return render(request,'faculty/assignment.html',context)


def facultyEvaluateAssignmentView(request,id):
    if request.method == "POST":
        grade = request.POST['assignmentMarks']
        student = request.POST['student']
        # assignment = request.POST['assignment']
        student = stud_details.objects.get(id=student)
        assignmentObject = assignment.objects.get(id=id)
        assignmentSubmissionObject = assignmentSubmission.objects.get(submitedBy=student,assignment=assignmentObject)
        if assignmentSubmissionObject.grade is not None:
            messages.info(request,'student Already graded')
            return redirect(f'/academic/ASSTPROF/lecture/{id}/viewSubmissions')
        else:
            assignmentSubmission.objects.filter(assignment=assignmentObject,submitedBy = student).update(grade=grade)
            messages.info(request,'graded Successfully')
            return redirect(f'/academic/ASSTPROF/lecture/{id}/viewSubmissions')



#------------------------------------------ controller of Examination ----------------------



def coeDepartmentView(request):
    if request.method == "POST":
        id = request.POST['department']
        subjectPacket = subjects.objects.filter(Department=Department.objects.get(id=id))
        context={
            'subjectPacket':subjectPacket
        }
        return render(request,'coe/departments.html',context)


def showDetails(request):
    if request.method == "POST":
        department = request.POST['department']
        subject = subjects.objects.filter(Department=department)
        quizReportPacket = quizGrades.objects.all()
        assignmentReportPacket = assignmentSubmission.objects.all()
        dataPacket = []
        count = 0
        for i in subject:
            quizPacket,assignmentPacket = 0,0
            quizPacket = quizReportPacket.filter(
                student__in = Subquery(lectureEnrollment.objects.filter(lecture=i).values('student')),
                quiz__in = Subquery(quizInfo.objects.filter(subject=i).values('id'))
            )
            print(quizPacket)
            assignmentPacket = assignmentReportPacket.filter(
                assignment__in = Subquery(assignment.objects.filter(subject=i).values('id'))
            )
            studentPacket = lectureEnrollment.objects.filter(lecture=i)
            scaledMarks = []
            for o in studentPacket:
                quizList = quizGrades.objects.filter(student=o.student).order_by('marks')
                print(quizList)
            dataPacket.append({
                'id':count,
                'subjectPacket':i,
                'quizReportPacket':quizPacket,
                'assignmentReportPacket':assignmentPacket,
                'studentPacket': studentPacket
            })
            count+=1
        context = {
            'subjectPacket' : subject,
            'coeSubjectView':True,
            'dataPacket':dataPacket
        }
        return render(request,'coe/marks.html',context)

def CoeScaleMarksView(request,id):
    subject= subjects.objects.get(id=id)
    quizReportPacket = quizGrades.objects.all()
    quizPacket = quizReportPacket.filter(
                student__in = Subquery(lectureEnrollment.objects.filter(lecture=subject).values('student'))
            ).order_by('marks')
    studentObject = lectureEnrollment.objects.filter(lecture=subject)
    mainPacket = []
    for i in studentObject:
        lst=[]
        quizDataPacket = quizPacket.filter(student=i.student).order_by('marks')
        print(len(quizDataPacket))
        if len(quizDataPacket)>=3:
            quizDataPacket = quizDataPacket[:3]
            for i in quizDataPacket:
                lst.append(i.marks)
        elif len(quizDataPacket)==2:
            quizDataPacket = quizDataPacket[:2]
            for i in quizDataPacket:
                lst.append(i.marks)
        elif len(quizDataPacket) == 1:
            quizDataPacket = quizDataPacket[:1]
            for i in quizDataPacket:
                lst.append(i.marks)
        else:
            messages.error(request,'Critical Failure at DB, Dirty values Occured!')
        print(lst)
        total=30
        print("total marks: ",sum(lst),"/",total)
        percent=(sum(lst)/total)*100
        # print("Percent out of 100%: ",percent,"%")

        cal_per=(percent/100)*(int(weightage.objects.get(mode=modes.objects.get(name="quiz")).percentage)*3)
        # print("marks obtained out of 15%: ",cal_per)
        arred = lambda x,n : x*(10**n)//1/(10**n)
        dataDictionary= {
            'student':i.student,
            'scaledMarks':arred(cal_per,2),
            'subject':subject
        }
        mainPacket.append(dataDictionary)
    context = {
        'mainPacket':mainPacket
    }
    return render(request,'coe/scale.html',context)


def coeScaleAssignmentMarksView(request,id):
    subject= subjects.objects.get(id=id)
    assignmentReportPacket = assignmentSubmission.objects.all()
    assignmentPacket = assignmentReportPacket.filter(
                submitedBy__in = Subquery(lectureEnrollment.objects.filter(lecture=subject).values('student'))
            ).order_by('grade')
    studentObject = lectureEnrollment.objects.filter(lecture=subject)
    mainPacket = []
    for i in studentObject:
        print("for",i.student.FullName)
        lst=[]
        assignmentDataPacket = assignmentPacket.filter(submitedBy=i.student).order_by('grade')
        print(len(assignmentDataPacket))
        if len(assignmentDataPacket)==2:
            assignmentDataPacket = assignmentDataPacket[:2]
            for j in assignmentDataPacket:
                lst.append(j.grade)
        elif len(assignmentDataPacket) == 1:
            assignmentDataPacket = assignmentDataPacket[:1]
            for j in assignmentDataPacket:
                lst.append(j.grade)
        else:
            messages.error(request,'Critical Failure at DB, Dirty values Occured!')
        print(lst)
        total=30
        # print("total marks: ",sum(lst),"/",total)
        percent=(sum(lst)/total)*100
        # print("Percent out of 100%: ",percent,"%")

        cal_per=(percent/100)*(int(weightage.objects.get(mode=modes.objects.get(name="quiz")).percentage)*3)
        # print("marks obtained out of 15%: ",cal_per)

        dataDictionary= {
            'student':i.student,
            'scaledMarks':cal_per,
            'subject':subject
        }
        mainPacket.append(dataDictionary)

    context = {
        'mainPacket':mainPacket
    }
    return render(request,'coe/scale.html',context)