from django.shortcuts import get_object_or_404, render,redirect

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.contrib import messages 
from django.core.files.storage import FileSystemStorage  
from django.urls import reverse 
from django.views.decorators.csrf import csrf_exempt 
from django.core import serializers 
import json 
from .forms import NotesForm


  
  
from .models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, FeedBackStaffs, StudentResult,Notes

def staff_home(request):
    return render(request,'faculty page/faculty_home.html')
def staff_notes(request):
    staff = Staffs.objects.get(admin=request.user.id) 
    uploaded_notes = Notes.objects.filter(uploaded_by=request.user.staffs)
    sessions = SessionYearModel.objects.all()
        
        
    subjects = Subjects.objects.filter(staff_id=request.user.id) 
       
        
    courses = Courses.objects.all() 
    
    context = { 
            "subjects": subjects, 
            "sessions": sessions,
            
            "courses" : courses,
            "uploaded_notes": uploaded_notes
           
        } 
    return render(request,'faculty page/notes.html',context)

def staff_profile(request): 
    user = CustomUser.objects.get(id=request.user.id) 
    staff = Staffs.objects.get(admin=user) 
  
    context={ 
        "user": user, 
        "staff": staff 
    } 
    return render(request, 'faculty page/profile.html', context) 
  
  
def staff_profile_update(request): 
    if request.method != "POST": 
        messages.error(request, "Invalid Method!") 
        return redirect('staff_profile') 
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
  
            staff = Staffs.objects.get(admin=customuser.id) 
            staff.address = address 
            staff.save() 
  
            messages.success(request, "Profile Updated Successfully") 
            return redirect('staff_profile') 
        except: 
            messages.error(request, "Failed to Update Profile") 
            return redirect('staff_profile') 

def staff_take_attendance(request): 
    subjects = Subjects.objects.filter(staff_id=request.user.id) 
    session_years = SessionYearModel.objects.all() 
    context = { 
        "subjects": subjects, 
        "session_years": session_years 
    } 
    return render(request, "faculty page/attendance.html", context)
 
def upload_notes(request):
    print("Inside upload_notes view function")  # Debugging statement
    
    try:
        staff = Staffs.objects.get(admin=request.user.id) 
        print("Staff:", staff)  # Debugging statement
        
        sessions = SessionYearModel.objects.all()
        print("Sessions:", sessions)  # Debugging statement
        
        subjects = Subjects.objects.filter(staff_id=request.user.id) 
        print("Subjects:", subjects)  # Debugging statement
        
        courses = Courses.objects.all() 
        print("Courses:", courses)  # Debugging statement
        
        if request.method == 'POST':
            print("Request method is POST")  # Debugging statement
            
            form = NotesForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.uploaded_by = staff
                form.save()
                print("Form saved successfully")  # Debugging statement
                return redirect('staff_notes')  # Redirect to the same page after form submission
            else:
                print("Form is not valid") 
                print("Form errors:", form.errors)  # D # Debugging statement
        else:
            print("Request method is not POST")  # Debugging statement
            form = NotesForm()
        
        context = { 
            "subjects": subjects, 
            "sessions": sessions,
            "form" : form,
            "courses" : courses
        } 
        return render(request, 'faculty page/notes.html', context)
    
    except Exception as e:
        print("Error:", e)  # Debugging statement
        return HttpResponse("An error occurred. Please try again later.")

def delete_notes(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    note.delete()
    return redirect('staff_notes')  # Redirect to the notes list page

def edit_notes(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    note_subject = note.subject_id.subject_name
    print(note_subject)
    if request.method == 'POST':
      
        form = NotesForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            print("valid form")
            
            form.save()
            print("form saved")
            return redirect('staff_notes') 
        else :

            print("invalid form")
            print("Form errors:", form.errors)
        # Redirect to the notes list page
    else:
        form = NotesForm(instance=note)
    
    context = {
        'form': form,
        'note': note,
        'note_subject': note_subject
    }
    return render(request, 'faculty page/notes.html', context)