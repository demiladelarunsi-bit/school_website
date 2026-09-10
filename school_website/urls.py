"""
URL configuration for school_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from portal import views

from django.contrib import admin
from django.urls import path
from portal import views

from django.contrib import admin
from django.urls import path, include

from django.urls import path
from portal import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/logout/', views.teacher_logout, name='teacher_logout'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/upload/', views.upload_result, name='upload_result'),
    path('teacher/delete/<int:pk>/', views.delete_result, name='delete_result'),
    path('student/check/', views.student_check, name='student_check'),
]