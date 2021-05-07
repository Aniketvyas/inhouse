from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

# Create your models here.

class employee(models.Model):
    id = models.AutoField(primary_key=True)
    EmployeeID = models.CharField(max_length=10)
    Email = models.EmailField()
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Dob = models.DateField()
    Doj = models.DateField()
    Etype = models.CharField(max_length=15)
    

    def __str__(self):
        return self.FirstName
    
class stud_details(models.Model):#Student Information
    id = models.AutoField(primary_key=True)
    EnrollmentNumber = models.CharField(max_length=10)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    MiddleName = models.CharField(max_length=100,blank=True)
    Department = models.ForeignKey('Department',on_delete=models.CASCADE)
    program = models.ForeignKey('program',on_delete=models.CASCADE)
    Specialization = models.CharField(max_length=35,blank=True)
    BatchYear = models.CharField(max_length=10)
    CurrSem = models.IntegerField()
    Residential =models.BooleanField()
    AccomodationID = models.BigIntegerField()
    UniversityEmailID = models.CharField(max_length=100)
    PersonalEmailID = models.CharField(max_length=100)
    Phone = models.BigIntegerField()
    StreetAddress = models.CharField(max_length=100)
    District = models.CharField(max_length=10)
    State = models.CharField(max_length=20)
    PinCode = models.IntegerField()
    ProtectedClass = models.CharField(max_length=3, blank=True)
    LastQualification = models.CharField(max_length=5)


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
    status = models.BooleanField()
    createdOn = models.DateTimeField(auto_now_add=True)

class lectures(models.Model):
    id = models.AutoField(primary_key=True)
    LectureID = models.CharField(max_length=10)
    LectureName = models.CharField(max_length=50)
    LessonPlan = models.FileField(upload_to='media')
    Semester = models.IntegerField()
    TaughtBy = models.ForeignKey('faculty' , on_delete=models.CASCADE, default=1)
    Credit = models.CharField(max_length=10)
    Department = models.ForeignKey('Department', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.LectureID

class lectureEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey('lectures',on_delete=models.CASCADE)
    student = models.ForeignKey('stud_details',on_delete=models.CASCADE)


class faculty(models.Model):
    id = models.AutoField(primary_key=True)
    FacultyID = models.CharField(max_length=10)
    Email = models.EmailField()
    Name = models.CharField(max_length=50)
    Ftype = models.CharField(max_length=30)
    Department = models.ForeignKey('Department',on_delete=models.CASCADE)
    FieldOfInterest1 = models.CharField(max_length=35)
    FieldOfInterest2 = models.CharField(max_length=35)
    FieldOfInterese3 = models.CharField(max_length=35)

    def __str__(self):
        return self.FacultyID


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


class attendence(models.Model):
    id = models.AutoField(primary_key=True)
    FacultyID = models.ForeignKey('faculty',on_delete=models.CASCADE)
    LastUpdatedOn = models.DateField()
    LectureID = models.ForeignKey('lectures',on_delete=models.CASCADE)
    attendanceFile = models.FileField(upload_to='attendance')


class lectureRecord(models.Model):
    id = models.AutoField(primary_key=True)
    lectureId = models.ForeignKey('lectures',on_delete=models.CASCADE)
    facultyId = models.ForeignKey('faculty',on_delete=models.CASCADE)
    goals = models.CharField(max_length=5000)
    status = models.CharField(max_length=20)
    startDate = models.DateField()
    endDate = models.DateField()
    notes = models.FileField()


  
