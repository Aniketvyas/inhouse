from django.conf import settings
from rest_framework import serializers
from academics.models import *



class stud_detailsSerializer(serializers.ModelSerializer):
     class Meta:
         model = stud_details
         fields = '__all__'


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

class lecturesSerializer(serializers.ModelSerializer):
    Department = departmentSerializer()
    TaughtBy = facultySerializer()
    class Meta:
        model = lectures
        fields = '__all__'

class lectureEnrollmentSerializer(serializers.ModelSerializer):
    lecture = lecturesSerializer()
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
    lecture = lecturesSerializer()
    faculty = facultySerializer()
    class Meta:
        model = lectureRecord
        fields = ' __all__'


