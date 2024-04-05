from django.shortcuts import render,redirect

from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib import messages 
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse 
import datetime 
from .models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult,Notes
def student_home(request):
    return render(request,'student page/student_home.html')
def student_profile(request): 
    user = CustomUser.objects.get(id=request.user.id) 
    student = Students.objects.get(admin=user) 
  
    context={ 
        "user": user, 
        "student": student 
    } 
    return render(request, 'student page/profile.html', context) 
  
  
def student_profile_update(request): 
    if request.method != "POST": 
        messages.error(request, "Invalid Method!") 
        return redirect('student_profile') 
    else: 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        password = request.POST.get('password') 
        address = request.POST.get('address') 
  
        try: 
            customuser = CustomUser.objects.get(id=request.user.id) 
            customuser.first_name = first_name 
            customuser.last_name = last_name 
            if password != None and password != "": 
                customuser.set_password(password) 
            customuser.save() 
  
            student = Students.objects.get(admin=customuser.id) 
            student.address = address 
            student.save() 
              
            messages.success(request, "Profile Updated Successfully") 
            return redirect('student_profile') 
        except: 
            messages.error(request, "Failed to Update Profile") 
            return redirect('student_profile') 
def student_notes(request):
    notes = Notes.objects.all()
    context = {
        "notes": notes
    }
    return render(request,'student page/notes.html',context)

def student_view_attendance(request): 
    
    # Getting Logged in Student Data 
    student = Students.objects.get(admin=request.user.id)  
      
    # Getting Course Enrolled of LoggedIn Student 
    course = student.course_id  
      
    # Getting the Subjects of Course Enrolled 
    subjects = Subjects.objects.filter(course_id=course)  
    context = { 
        "subjects": subjects 
    } 
    return render(request, "student page/attendance.html", context) 

def student_view_attendance_post(request): 
    if request.method != "POST": 
        messages.error(request, "Invalid Method") 
        return redirect('student_view_attendance') 
    else: 
        # Getting all the Input Data 
        subject_id = request.POST.get('subject') 
        start_date = request.POST.get('start_date') 
        end_date = request.POST.get('end_date') 
  
        # Parsing the date data into Python object 
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() 
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() 
  
        # Getting all the Subject Data based on Selected Subject 
        subject_obj = Subjects.objects.get(id=subject_id) 
          
        # Getting Logged In User Data 
        user_obj = CustomUser.objects.get(id=request.user.id) 
          
        # Getting Student Data Based on Logged in Data 
        stud_obj = Students.objects.get(admin=user_obj) 
  
        # Now Accessing Attendance Data based on the Range of Date 
        # Selected and Subject Selected 
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, 
                                                                       end_date_parse), 
                                               subject_id=subject_obj) 
        # Getting Attendance Report based on the attendance 
        # details obtained above 
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, 
                                                             student_id=stud_obj) 
  
          
        context = { 
            "subject_obj": subject_obj, 
            "attendance_reports": attendance_reports,
            "user" : stud_obj,
        } 
  
        return render(request, 'student page/student_attendance_data.html', context) 
         
  