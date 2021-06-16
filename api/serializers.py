from django.conf import settings
from rest_framework import serializers
from academics.models import *





class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = '__all__'

class facultySerializer(serializers.ModelSerializer):
    class Meta:
        model = faculty
        fields = '__all__'

class schoolSerializer(serializers.ModelSerializer):
    dean = employeeSerializer()
    class Meta:
        model = school
        fields = ['id','name','status',"dean"]

class programSerializer(serializers.ModelSerializer):
    # school = serializers.StringRel/atedField()
    school = schoolSerializer(read_only=True)
    class Meta:
        model = program
        fields = '__all__'
    def get_school(self, obj):
        return obj.school.name


class departmentSerializer(serializers.ModelSerializer):
    # Program = programSerializer()
    HeadOfDepartment = employeeSerializer()
    class Meta:
        model = Department
        fields = '__all__'

class stud_detailsSerializer(serializers.ModelSerializer):
    Department = departmentSerializer()
    program = programSerializer()
    class Meta:
        model = stud_details
        fields = '__all__'


class subjectsSerailizer(serializers.ModelSerializer):
    Department = departmentSerializer()
    TaughtBy = facultySerializer()
    class Meta:
        model = subjects
        fields = "__all__"

class lectureEnrollmentSerializer(serializers.ModelSerializer):
    subjects = subjectsSerailizer()
    student = stud_detailsSerializer()
    class Meta:
        model = lectureEnrollment
        fields = '__all__'



class tempLecturesSerailizer(serializers.ModelSerializer):
    class Meta:
        model = TempLectures
        fields = '__all__'
    


# class attendanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = attendance
#         fields = '__all__'


class lectureRecordSerializer(serializers.ModelSerializer):
    subject = subjectsSerailizer()
    faculty = facultySerializer()
    class Meta:
        model = lectureRecord
        fields = ' __all__'


class modesSerializer(serializers.ModelSerializer):
    class Meta:
        model=  modes
        field = "__all__"

class weightageSerializer(serializers.ModelSerializer):
    mode = modesSerializer()
    subject = subjectsSerailizer()
    faculty = facultySerializer()
    class Meta:
        model=weightage
        fields = "__all__"
class quizInfoSerializer(serializers.ModelSerializer):
    subject = subjectsSerailizer()
    class Meta:
        model = quizInfo
        fields = "__all__"

class quizQuestionsSerializer(serializers.ModelSerializer):
    quiz = quizInfoSerializer()
    class Meta:
        model = quizQuestions
        fields = "__all__"

class quizGradesSerializer(serializers.ModelSerializer):
    quiz = quizInfoSerializer()
    student = stud_detailsSerializer()
    class Meta:
        model = quizGrades
        fields = "__all__"

class assignmentSerializer(serializers.ModelSerializer):
    subject = subjectsSerailizer()
    class Meta:
        model = assignment
        fields =  "__all__"

class assignmentSubmissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = assignmentSubmission
        fields = "__all__"

    
