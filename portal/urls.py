from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/logout/', views.teacher_logout, name='teacher_logout'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/upload/', views.upload_result, name='upload_result'),
    path('teacher/view/<int:pk>/', views.view_result_card, name='view_result_card'),
    path('teacher/delete/<int:pk>/', views.delete_result, name='delete_result'),
    path('student/check/', views.student_check, name='student_check'),
]