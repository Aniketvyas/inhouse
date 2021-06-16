from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    #--------------MAIN ACADEMICS-------------------
    path('dashboard',views.home),
    # path('<str:id>',views.Etype),
    path('lecture/view',views.lecture),
    path('lecture/AddLecture',views.AddLecture),
    path('lecture/RemoveLecture',views.remove),
   
      
    # path('department/<str:id>/view',views.deanDepartmentView),
    path('department/<str:id/faculty',views.DepartmentFaculty),
    path('faculty/info',views.faculty_info),

    #----------------Assistant professors--------------

    path('ASSTPROF/lecture/view',views.asstlecture),
    path('ASSTPROF/lecture/<str:lecture>/view',views.assLectureView),
    path('ASSTPROF/lecture/lectureRequest',views.lectureRequest),
    path('ASSTPROF/lecture/lectureRequestData',views.lectureRequest),
    path('ASSTPROF/lecture/lectureStatus',views.lectureStatus),
    path('ASSTPROF/lecture/<int:id>/lectureChangedData',views.lectureChangeInfo),
    path('ASSTPROF/lecture/<str:id>/Track',views.trackLecture),
    path('ASSTPROF/lecture/<str:id>/goalsInfo',views.trackLecture),
    #------------- Quiz -------------------------
    path('ASSTPROF/lecture/hostQuiz',views.quizHost),
    path('ASSTPROF/lecture/quiz/<str:id>/enterQuestions/<str:questionType>',views.enterQuestions),
    path('ASSTPROF/lecture/previousQuiz',views.previousQuiz),
    path('ASSTPROF/lecture/previousQuiz/<str:id>/<str:command>/<str:questionType>',views.previousQuizDetails),
    path('ASSTPROF/lecture/previousQuiz/<str:quizId>/deleteQuestions/delete/<str:questionId>',views.deleteQuestions),
    path('ASSTPROF/lecture/previousQuiz/<str:id>/updateQuestion/<str:questionType>/<str:questionId>',views.updateQuestions),
    # path('ASSTPROF/lecture/quiz/<str:id>/quizQuestions',views.enterQuestions),
    # path('ASSTPROF/lecture/quiz/<str:id>/enterQuestions/<str:questionType>',views.enterQuestions),
    # path('ASSTPROF/lecture/quiz/<str:id>/enterQuestions/<str:questionType>',views.enterQuestions),
    # path('ASSTPROF/lecture/previousQuiz/<str:id>/ViewDetails',views.previousQuizDetails),
    # path('ASSTPROF/lecture/previousQuiz/<str:id>/update/mcq',views.updateMcqQuestions),
    # path('ASSTPROF/lecture/previousQuiz/<str:quizID>/<str:questionID>/delete',views.deleteQuestions),
    # path('ASSTPROF/lecture/previousQuiz/<str:id>/quizQuestions/mcq',views.addQuestionsMcq),
    # path('ASSTPROF/lecture/previousQuiz/<str:id>/quizQuestions/nat',views.addQuestionsNat),

    #------------------ ASsignments -------------------
    path('ASSTPROF/lecture/createAssignment',views.createAssignments),
    path('ASSTPROF/lecture/previousAssignments',views.previousAssignment),
    path('ASSTPROF/lecture/previousAssignment/<str:id>/update',views.updatePreviousAssignment),
    path('ASSTPROF/lecture/previousAssignment/<str:id>/delete',views.deletePreviousAssignment),
    path('ASSTPROF/lecture/<int:id>/viewSubmissions',views.facultyAssignmentSubmissionView),
    path('ASSTPROF/lecture/<str:id>/evaluateAssignment',views.facultyEvaluateAssignmentView),
  

    #-----------------Head Of Department-----------------------

    path('HOD/lecture/view',views.hodLecture),
    path('HOD/lecture/<str:id>/assignFaculty',views.HodAssignFaculty),
    path('HOD/lecture/create',views.createLecture),
    # path('HOD/lecture/lectureRequest',views.HodLectureRequest),
    # path('HOD/lecture/<str:id>/update',views.lectureChangeRequest),
    # path('HOD/lecture/<str:id>/Approve',views.lectureApproveRequest),
    # path('HOD/lecture/<str:id>/Configure',views.lectureConfigureRequest),
    # path('HOD/Outpass/requests',views.OutpassRequests),
    path('HOD/Enrollment',views.LectureEnrollments),
    path('HOD/Enrollment/<str:id>',views.LectureEnrollmentSecond),
    # path('HOD/lecture/<str:id>/filter',views.lectureFilter),
    # path('HOD/lecture/<str:LectureID>/Enroll/<str:EnrollmentNumber>',views.LectureEnrollmentDone),
    path('HOD/lecture/<int:lecture>/view',views.lol),
    path('HOD/lecture/<str:id>/Track',views.trackLectureHod),

    #-----------------DEAN OF ENGINEERING ---------------------
    path('dean/department/info',views.deanDepartmentView), 
    path('dean/department/<int:id>/view',views.deanDepartmentDetailView),
    path('dean/lecture/view',views.deanLecture),
    path('dean/lecture/lectureRequest',views.DeanLectureRequest),
    path('dean/lecture/lectureOngoing',views.DeanOngoingRequest),
    path('dean/lecture/<int:id>/update',views.lectureChangeRequest),
    path('dean/lecture/<int:id>/Approve',views.lectureApproveRequest),
    path('dean/lecture/<int:id>/Configure',views.lectureConfigureRequest),

    #--------------------VICE - CHANCELLOR -----------------------

    path('vc/lecture/view',views.lectureView),
    path('vc/lecture/lectureRequest',views.vclectureRequest),
    path('vc/lecture/<int:id>/update',views.lectureChangeRequest),
    path('vc/lecture/<int:id>/Approve',views.lectureApproveVc),

#----------------------- STUDENTS ------------------------------------
    path('student/lecture',views.studentLectureView),
    path('student/quizStudentView',views.quizStudentView),
    path('student/<str:id>/quizDetailView',views.quizDetailView),
    path('student/assignmentStudentView',views.assignmentStudentView),
    path('student/<str:id>/submitAssignment',views.studentAssignmentSubmitView),
    path('student/<str:id>/updateAssignment',views.studentUpdateAssignmentView),
    path('student/<str:lecture>/track',views.studentTrackView),
    # path('student/')

#------------------------ COE ----------------------------------------
    # path('coe/academics',views.coeDepartmentView),
    path('coe/departmentView',views.coeDepartmentView),
    path('coe/marksView',views.showDetails),
    # path('coe/showDetails',views.)
   

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)