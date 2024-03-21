from django.contrib import admin
from django.urls import path,include
from .import views
from .import HodViews,StudentViews,StaffViews
urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.home,name='home.html'),
    
    path('login', views.loginUser, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
    path('hod_home/', HodViews.hod_home, name="hod_home"),
    path('add_staff_save/', HodViews.add_staff_save, name="add_staff_save"),
    path('add_staff/', HodViews.add_staff, name="add_staff"),
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('staff_home/', StaffViews.staff_home, name="staff_home"), 
    path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
    path('manage_staff/', HodViews.manage_staff, name="manage_staff"), 
    path('edit_staff/<staff_id>/', HodViews.edit_staff, name="edit_staff"), 
    path('edit_staff_save/', HodViews.edit_staff_save, name="edit_staff_save"), 
    path('delete_staff/<staff_id>/', HodViews.delete_staff, name="delete_staff"),
    path('add_course/', HodViews.add_course, name="add_course"), 
    path('add_course_save/', HodViews.add_course_save, name="add_course_save"), 
    path('manage_course/', HodViews.manage_course, name="manage_course"), 
    path('edit_course/<course_id>/', HodViews.edit_course, name="edit_course"), 
    path('edit_course_save/', HodViews.edit_course_save, name="edit_course_save"), 
    path('delete_course/<course_id>/', HodViews.delete_course, name="delete_course"), 
    path('manage_session/', HodViews.manage_session, name="manage_session"), 
    path('add_session/', HodViews.add_session, name="add_session"), 
    path('add_session_save/', HodViews.add_session_save, name="add_session_save"), 
    path('edit_session/<session_id>', HodViews.edit_session, name="edit_session"), 
    path('edit_session_save/', HodViews.edit_session_save, name="edit_session_save"), 
    path('delete_session/<session_id>/', HodViews.delete_session, name="delete_session"), 
]
