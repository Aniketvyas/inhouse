from django.db import models
from django.conf import settings
from django.db.models.base import ModelState

# Create your models here.

class employee(models.Model):
    id = models.AutoField(primary_key=True)
    employeeID = models.CharField(max_length=10)
    personalEmail = models.EmailField()
    universityEmail = models.EmailField(blank=True)
    Name = models.CharField(max_length=20)
    Dob = models.DateField()
    Doj = models.DateField()


    def __str__(self):
        return self.Name

class stud_details(models.Model):#Student Information
    id = models.AutoField(primary_key=True)
    EnrollmentNumber = models.CharField(max_length=10)
    FullName = models.CharField(max_length=100)
    Department = models.ForeignKey('Department',on_delete=models.CASCADE)
    program = models.ForeignKey('program',on_delete=models.CASCADE)
    BatchYear = models.CharField(max_length=10)
    UniversityEmailID = models.CharField(max_length=100)
    PersonalEmailID = models.CharField(max_length=100)
    Phone = models.BigIntegerField()
    currentSemester = models.IntegerField(blank=True)
    StreetAddress = models.CharField(max_length=100)
    District = models.CharField(max_length=10)
    State = models.CharField(max_length=20)
    PinCode = models.IntegerField()
    LastQualification = models.CharField(max_length=100)


    def __str__(self):
        return self.EnrollmentNumber


class school(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dean = models.ForeignKey('employee',on_delete=models.CASCADE)
    status = models.BooleanField()
    createdOn = models.DateTimeField(auto_now_add=True)


class program(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    school = models.ForeignKey('school',on_delete=models.CASCADE)
    totalSemester = models.IntegerField(blank=True)
    status = models.BooleanField()
    createdOn = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subjectCode = models.CharField(max_length=10)
    subjectName = models.CharField(max_length=50)
    LessonPlan = models.FileField(upload_to='media')
    Semester = models.IntegerField()
    TaughtBy = models.ForeignKey('faculty' , on_delete=models.CASCADE,blank=True)
    Credit = models.CharField(max_length=10)
    Department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.subjectCode + " "+ self.subjectName

class lectureEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey('subjects',on_delete=models.CASCADE)
    student = models.ForeignKey('stud_details',on_delete=models.CASCADE)

    def __str__(self):
        return self.student.FullName + " of "+ str(self.student.currentSemester) + " sem Enrolled in " + self.lecture.subjectName

class faculty(models.Model):
    id = models.AutoField(primary_key=True)
    FacultyID = models.ForeignKey('employee',on_delete=models.CASCADE)
    Department = models.ForeignKey('Department',on_delete=models.CASCADE)

    def __str__(self):
        return self.FacultyID.Name


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    DepartmentID = models.CharField(max_length=10)
    DepartmentName = models.CharField(max_length=100)
    HeadOfDepartment = models.ForeignKey('employee',on_delete=models.CASCADE)
    SpecializedCourse = models.BooleanField()
    StartDate = models.DateField()
    School = models.ForeignKey('school',on_delete=models.CASCADE)
    Status = models.BooleanField()

    def __str__(self):
        return self.DepartmentID


class TempLectures(models.Model):
    id = models.AutoField(primary_key=True)
    TempLectureID = models.CharField(max_length=15)
    LectureTitle = models.CharField(max_length=500)
    Semester = models.IntegerField()
    Credit = models.CharField(max_length=10)
    TempLessonPlan = models.FileField(upload_to='media')
    CreatedBy = models.EmailField()
    Department = models.ForeignKey('Department',on_delete=models.CASCADE)
    LectureStatus = models.CharField(max_length=15)
    Changes = models.FileField(upload_to='media')
    LastChangesMadeBy = models.CharField(max_length=30)
    LastApprovedBy = models.CharField(max_length=30)
    NextSendTo = models.CharField(max_length=15)


class modes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class weightage(models.Model):
    id = models.AutoField(primary_key=True)
    mode = models.ForeignKey('modes',on_delete=models.CASCADE)
    subjects = models.ForeignKey('subjects',on_delete=models.CASCADE)
    percentage = models.CharField(max_length=5)
    assignedBy = models.ForeignKey('faculty',on_delete=models.CASCADE)
    validTill = models.DateField(null=True,blank=True)
    assignedOn = models.DateTimeField()

    def __str__(self):
        return self.mode.name + " - " + self.percentage + "%"


class quizInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    quizDate = models.DateField()
    quizStartTime = models.TimeField()
    quizEndTime = models.TimeField()
    duration = models.IntegerField()
    subject = models.ForeignKey('subjects',on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class quizQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey('quizInfo',on_delete=models.CASCADE)
    question = models.TextField()
    questionType = models.CharField(max_length=40)
    option1 = models.CharField(max_length=1000)
    option2 = models.CharField(max_length=1000)
    option3 = models.CharField(max_length=1000)
    option4 = models.CharField(max_length=1000)
    correctOption = models.CharField(max_length=1000)

    def __str__(self):
        return " "+ self.question + " " + self.option1+ " "+ self.option2+ " "+ self.option3+" "+ self.option4+" "+self.correctOption

class quizGrades(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey('quizInfo',on_delete=models.CASCADE)
    student = models.ForeignKey('stud_details',on_delete=models.CASCADE)
    unAttemptedQuestions = models.IntegerField(null=True)
    wrongAnswers = models.IntegerField(null=True)
    correctAnswers = models.IntegerField(null=True)
    timeTaken = models.CharField(max_length=100,null=True,blank=True)
    startedOn = models.DateTimeField(null=True,blank=True) 
    submitedOn = models.DateTimeField(auto_now_add=True,null=True)
    marks = models.IntegerField()

    def __str__(self):
        return self.quiz.name + " "+ self.student.FullName


class assignment(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
    ('CA', 'Class'),
    ('HA', 'Home')
]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    assignmentType = models.CharField(choices = YEAR_IN_SCHOOL_CHOICES,null=True,max_length=2)
    assignmentFile = models.FileField()
    subject = models.ForeignKey('subjects',on_delete=models.CASCADE)
    startingDate = models.DateField(null=True)
    deadline = models.DateField(null=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class assignmentSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey('assignment',on_delete=models.CASCADE)
    submissionFile = models.FileField()
    submitedBy = models.ForeignKey('stud_details',on_delete=models.CASCADE)
    submitedOn = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(blank=True,null=True)
    def __str__(self) -> str:
        return str(self.id)+" " + self.assignment.name +" "+ self.assignment.subject.subjectName+ " " + self.submitedBy.FullName

class attendance(models.Model):
    id = models.AutoField(primary_key=True)
    attendies = models.ForeignKey('stud_details',on_delete=models.CASCADE)
    subject = models.ForeignKey('subjects',on_delete=models.CASCADE)
    takenOn = models.DateTimeField(auto_now_add=True)

class lectureRecord(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('subjects',on_delete=models.CASCADE)
    faculty = models.ForeignKey('faculty',on_delete=models.CASCADE)
    goals = models.CharField(max_length=5000)
    status = models.CharField(max_length=20)
    startDate = models.DateField()
    endDate = models.DateField()
    notes = models.FileField()



