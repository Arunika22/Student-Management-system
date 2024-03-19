from django.shortcuts import render,redirect

def student_home(request):
    return render(request,'student page/student_home.html')