from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib import admin
from .models import Result, Subject

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 3

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('exam_number', 'student_name', 'year', 'term', 'class_name', 'average_mark', 'grade')
    list_filter = ('year', 'term', 'class_name', 'grade')
    search_fields = ('exam_number', 'student_name')
    inlines = [SubjectInline]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('result', 'subject_name', 'marks', 'grade')
    search_fields = ('subject_name',)