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

    session_id = request.GET.get('session')
    subject_id = request.GET.get('subject')
    date = request.GET.get('date')

    contexts={
        'subjects' : subjects,
        "session_years" : session_years
    }

    if session_id and subject_id : 
        session = SessionYearModel.objects.get(id=session_id)
        subject = Subjects.objects.get(id=subject_id)
        students = Students.objects.filter(course_id=subject.course_id,session_year_id=session.id)
        attendance = Attendance.objects.filter(session_year_id=session.id,subject_id=subject.id, attendance_date=date).first()
        
        contexts['active_session'] = session
        contexts['active_subject'] = subject
        contexts['date'] = date
        contexts['students'] = students
        contexts['attendance'] = attendance
        if attendance != None :
            attendance_report = AttendanceReport.objects.filter(attendance_id=attendance.id)
            contexts['attendace_report'] = attendance_report
        

    return render(request, "faculty page/attendance.html", contexts)

def add_attendance(request):
    subject_id = request.POST.get('subject_id')
    session_id = request.POST.get('session_id')
    attendance_date = request.POST.get('date')
    students = request.POST.getlist('student[]')
    attendanceStatus = request.POST.getlist('attendance[]')

    subject = Subjects.objects.get(id=subject_id)
    session_year = SessionYearModel.objects.get(id=session_id)

    attendance = Attendance.objects.create(subject_id=subject,session_year_id=session_year,attendance_date=attendance_date)
    for index in range(len(students)) : 
        student = Students.objects.get(id=students[index])
        status = attendanceStatus[index]

        # storing individual attendance
        AttendanceReport.objects.create(
            student_id=student,
            attendance_id=attendance,
            status=(True if status=='true' else False)
        )

    return staff_take_attendance(request);

def edit_attendance(request) :
    if request.method != "POST": 
        return HttpResponse("Invalid Method!") 
    
    attendance_id = request.POST.get('attendance_id')
    record_ids = request.POST.getlist('record_id[]')
    attendanceStatus = request.POST.getlist('attendance[]')

    for index in range(len(record_ids)) : 
        report = AttendanceReport.objects.get(id=record_ids[index])
        report.status = True if attendanceStatus[index]=='true' else False

        report.save()

    return staff_take_attendance(request);

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
# def staff_take_attendance(request): 
#     subjects = Subjects.objects.filter(staff_id=request.user.id) 
#     session_years = SessionYearModel.objects.all() 
#     context = { 
#         "subjects": subjects, 
#         "session_years": session_years 
#     } 
#     return render(request, "faculty page/attendance.html", context) 
# @csrf_exempt
# def save_attendance_data(request): 
    
#     # Get Values from Staf Take Attendance form via AJAX (JavaScript) 
#     # Use getlist to access HTML Array/List Input Data 
#     student_ids = request.POST.get("student_ids") 
#     subject_id = request.POST.get("subject_id") 
#     attendance_date = request.POST.get("attendance_date") 
#     session_year_id = request.POST.get("session_year_id") 
  
#     subject_model = Subjects.objects.get(id=subject_id) 
#     session_year_model = SessionYearModel.objects.get(id=session_year_id) 
  
#     json_student = json.loads(student_ids) 
      
#     try: 
#         # First Attendance Data is Saved on Attendance Model 
#         attendance = Attendance(subject_id=subject_model, 
#                                 attendance_date=attendance_date, 
#                                 session_year_id=session_year_model) 
#         attendance.save() 
  
#         for stud in json_student: 
#             # Attendance of Individual Student saved on AttendanceReport Model 
#             student = Students.objects.get(admin=stud['id']) 
#             attendance_report = AttendanceReport(student_id=student, 
#                                                  attendance_id=attendance, 
#                                                  status=stud['status']) 
#             attendance_report.save() 
#         return HttpResponse("OK") 
#     except: 
#         return HttpResponse("Error") 
  
  
  
  
# def staff_update_attendance(request): 
#     subjects = Subjects.objects.filter(staff_id=request.user.id) 
#     session_years = SessionYearModel.objects.all() 
#     context = { 
#         "subjects": subjects, 
#         "session_years": session_years 
#     } 
#     return render(request, "faculty page/attendance.html", context) 

# @csrf_exempt
# def get_students(request): 
    
#     subject_id = request.POST.get("subject") 
#     session_year = request.POST.get("session_year") 
  
#     # Students enroll to Course, Course has Subjects 
#     # Getting all data from subject model based on subject_id 
#     subject_model = Subjects.objects.get(id=subject_id) 
  
#     session_model = SessionYearModel.objects.get(id=session_year) 
  
#     students = Students.objects.filter(course_id=subject_model.course_id, 
#                                        session_year_id=session_model) 
  
#     # Only Passing Student Id and Student Name Only 
#     list_data = [] 
  
#     for student in students: 
#         data_small={"id":student.admin.id, 
#                     "name":student.admin.first_name+" "+student.admin.last_name} 
#         list_data.append(data_small) 
  
#     return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False) 
  
# @csrf_exempt
# def save_attendance_data(request): 
    
#     # Get Values from Staf Take Attendance form via AJAX (JavaScript) 
#     # Use getlist to access HTML Array/List Input Data 
#     student_ids = request.POST.get("student_ids") 
#     subject_id = request.POST.get("subject_id") 
#     attendance_date = request.POST.get("attendance_date") 
#     session_year_id = request.POST.get("session_year_id") 
  
#     subject_model = Subjects.objects.get(id=subject_id) 
#     session_year_model = SessionYearModel.objects.get(id=session_year_id) 
  
#     json_student = json.loads(student_ids) 
      
#     try: 
#         # First Attendance Data is Saved on Attendance Model 
#         attendance = Attendance(subject_id=subject_model, 
#                                 attendance_date=attendance_date, 
#                                 session_year_id=session_year_model) 
#         attendance.save() 
  
#         for stud in json_student: 
#             # Attendance of Individual Student saved on AttendanceReport Model 
#             student = Students.objects.get(admin=stud['id']) 
#             attendance_report = AttendanceReport(student_id=student, 
#                                                  attendance_id=attendance, 
#                                                  status=stud['status']) 
#             attendance_report.save() 
#         return HttpResponse("OK") 
#     except: 
#         return HttpResponse("Error") 
  
  
# @csrf_exempt
# def get_attendance_dates(request): 
      
  
#     # Getting Values from Ajax POST 'Fetch Student' 
#     subject_id = request.POST.get("subject") 
#     session_year = request.POST.get("session_year_id") 
  
#     # Students enroll to Course, Course has Subjects 
#     # Getting all data from subject model based on subject_id 
#     subject_model = Subjects.objects.get(id=subject_id) 
  
#     session_model = SessionYearModel.objects.get(id=session_year) 
#     attendance = Attendance.objects.filter(subject_id=subject_model, 
#                                            session_year_id=session_model) 
  
#     # Only Passing Student Id and Student Name Only 
#     list_data = [] 
  
#     for attendance_single in attendance: 
#         data_small={"id":attendance_single.id, 
#                     "attendance_date":str(attendance_single.attendance_date), 
#                     "session_year_id":attendance_single.session_year_id.id} 
#         list_data.append(data_small) 
  
#     return JsonResponse(json.dumps(list_data), 
#                         content_type="application/json", safe=False) 
  
  
# @csrf_exempt
# def get_attendance_student(request): 
    
#     # Getting Values from Ajax POST 'Fetch Student' 
#     attendance_date = request.POST.get('attendance_date') 
#     attendance = Attendance.objects.get(id=attendance_date) 
  
#     attendance_data = AttendanceReport.objects.filter(attendance_id=attendance) 
#     # Only Passing Student Id and Student Name Only 
#     list_data = [] 
  
#     for student in attendance_data: 
#         data_small={"id":student.student_id.admin.id, 
#                     "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status} 
#         list_data.append(data_small) 
  
#     return JsonResponse(json.dumps(list_data), 
#                         content_type="application/json", 
#                         safe=False) 
  
  
# @csrf_exempt
# def update_attendance_data(request): 
#     student_ids = request.POST.get("student_ids") 
  
#     attendance_date = request.POST.get("attendance_date") 
#     attendance = Attendance.objects.get(id=attendance_date) 
  
#     json_student = json.loads(student_ids) 
  
#     try: 
          
#         for stud in json_student: 
            
#             # Attendance of Individual Student saved on AttendanceReport Model 
#             student = Students.objects.get(admin=stud['id']) 
  
#             attendance_report = AttendanceReport.objects.get(student_id=student, 
#                                                              attendance_id=attendance) 
#             attendance_report.status=stud['status'] 
  
#             attendance_report.save() 
#         return HttpResponse("OK") 
#     except: 
#         return HttpResponse("Error") 
  