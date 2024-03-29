from django.contrib import admin
from django.urls import path,include
from .import views
from .import HodViews,StudentViews,StaffViews
from django.conf import settings
from django.conf.urls.static import static
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
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
     path('student_notes/', StudentViews.student_notes, name="student_notes"), 
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"), 
    
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
     path('add_student_save/', HodViews.add_student_save, name="add_student_save"), 
    path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"), 
    path('add_student/', HodViews.add_student, name="add_student"),
    path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"), 
    path('manage_student/', HodViews.manage_student, name="manage_student"), 
    path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
     path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"), 
    path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"), 
    path('add_subject/', HodViews.add_subject, name="add_subject"), 
    path('add_subject_save/', HodViews.add_subject_save, name="add_subject_save"), 
    path('manage_subject/', HodViews.manage_subject, name="manage_subject"), 
    path('edit_subject/<subject_id>/', HodViews.edit_subject, name="edit_subject"), 
    path('edit_subject_save/', HodViews.edit_subject_save, name="edit_subject_save"), 
    path('delete_subject/<subject_id>/', HodViews.delete_subject, name="delete_subject"), 
    #faculty urls
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
     path('staff_notes/', StaffViews.staff_notes, name="staff_notes"), 
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"), 
    path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"), 
    path('staff_take_attendance/', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('upload_notes/', StaffViews.upload_notes, name="upload_notes"),
    path('edit_notes/<int:note_id>/', StaffViews.edit_notes, name='edit_notes'),
    path('delete_notes/<int:note_id>/', StaffViews.delete_notes, name='delete_notes'),
   
     
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)