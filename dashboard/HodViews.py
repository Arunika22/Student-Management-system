from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
 
from .forms import AddStudentForm, EditStudentForm
 
from .models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport
 
def hod_home(request):
    return render(request,'Hod Page/hod_home.html')

def add_staff(request) :
    return render(request,"Hod Page/add_staff.html")

def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        email = request.POST.get('email')
        print("Email:", email) 
        username = request.POST.get('username')
        print("Username:", username)
        password = request.POST.get('password')
        print("password:", password)
        first_name = request.POST.get('first_name')
        print("first_name:", first_name)
        last_name = request.POST.get('last_name')
        
        print("last_name:", last_name)
        address = request.POST.get('address')
 
        try:
            user = CustomUser.objects.create(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
            
            staff = Staffs.objects.create(admin=user, address=address)
            
            messages.success(request, "Staff Added Successfully!")
            
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')
 
def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "Hod Page/manage_faculty.html", context)