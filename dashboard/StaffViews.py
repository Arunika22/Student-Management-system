from django.shortcuts import render,redirect

def staff_home(request):
    return render(request,'faculty page/faculty_home.html')