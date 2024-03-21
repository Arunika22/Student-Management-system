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



 
def edit_staff(request, staff_id): 
    staff = Staffs.objects.get(admin=staff_id) 
  
    context = { 
        "staff": staff, 
        "id": staff_id 
    } 
    return render(request, "Hod Page/edit_staff_template.html", context) 
  
  
def edit_staff_save(request): 
    if request.method != "POST": 
        return HttpResponse("<h2>Method Not Allowed</h2>") 
    else: 
        staff_id = request.POST.get('staff_id') 
        username = request.POST.get('username') 
        email = request.POST.get('email') 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        address = request.POST.get('address') 
  
        try: 
            # INSERTING into Customuser Model 
            user = CustomUser.objects.get(id=staff_id) 
            user.first_name = first_name 
            user.last_name = last_name 
            user.email = email 
            user.username = username 
            user.save() 
              
            # INSERTING into Staff Model 
            staff_model = Staffs.objects.get(admin=staff_id) 
            staff_model.address = address 
            staff_model.save() 
  
            messages.success(request, "Staff Updated Successfully.") 
            return redirect('/edit_staff/'+staff_id) 
  
        except: 
            messages.error(request, "Failed to Update Staff.") 
            return redirect('/edit_staff/'+staff_id) 
  
  
  
def delete_staff(request, staff_id): 
    staff = Staffs.objects.get(admin=staff_id) 
    try: 
        staff.delete() 
        messages.success(request, "Staff Deleted Successfully.") 
        return redirect('manage_staff') 
    except: 
        messages.error(request, "Failed to Delete Staff.") 
        return redirect('manage_staff') 
  

def add_course(request): 
    return render(request, "Hod Page/add_course.html") 

def add_course_save(request): 
    if request.method != "POST": 
        messages.error(request, "Invalid Method!") 
        return redirect('add_course') 
    else: 
        course = request.POST.get('course') 
        try: 
            course_model = Courses(course_name=course) 
            course_model.save() 
            messages.success(request, "Course Added Successfully!") 
            return redirect('add_course') 
        except: 
            messages.error(request, "Failed to Add Course!") 
            return redirect('add_course') 
  
  
def manage_course(request): 
    courses = Courses.objects.all() 
    context = { 
        "courses": courses 
    } 
    return render(request, 'Hod Page/manage_course.html', context) 
  
  
def edit_course(request, course_id): 
    course = Courses.objects.get(id=course_id) 
    context = { 
        "course": course, 
        "id": course_id 
    } 
    return render(request, 'hod_template/edit_course_template.html', context) 
  
  
def edit_course_save(request): 
    if request.method != "POST": 
        HttpResponse("Invalid Method") 
    else: 
        course_id = request.POST.get('course_id') 
        course_name = request.POST.get('course') 
  
        try: 
            course = Courses.objects.get(id=course_id) 
            course.course_name = course_name 
            course.save() 
  
            messages.success(request, "Course Updated Successfully.") 
            return redirect('/edit_course/'+course_id) 
  
        except: 
            messages.error(request, "Failed to Update Course.") 
            return redirect('/edit_course/'+course_id) 
  
  
def delete_course(request, course_id): 
    course = Courses.objects.get(id=course_id) 
    try: 
        course.delete() 
        messages.success(request, "Course Deleted Successfully.") 
        return redirect('manage_course') 
    except: 
        messages.error(request, "Failed to Delete Course.") 
        return redirect('manage_course') 
  
  
