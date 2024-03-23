from django.shortcuts import render,redirect

from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib import messages 
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse 
import datetime 
from .models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult 
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
    return render(request,'student page/notes.html')