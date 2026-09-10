from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Result, Subject
from .forms import ResultUploadForm, StudentCheckForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Result, Subject
from .forms import ResultUploadForm, StudentCheckForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Result, Subject
from .forms import ResultUploadForm, StudentCheckForm

# MAKE SURE THIS LIST IS HERE
SUBJECTS_LIST = [
    "Mathematics", "English Language", "Civic Education", "Basic Science", "Basic Technology",
    "Social Studies", "Computer Studies", "Agricultural Science", "Business Studies", "Fine Arts",
    "French", "C.R.K", "I.R.K", "Physics", "Chemistry", "Biology", "Economics", "Government",
    "Geography", "Literature in English", "Further Mathematics"
]

def calculate_grade(mark):
    if mark >= 90: return 'A+'
    elif mark >= 80: return 'A'
    elif mark >= 70: return 'B+'
    elif mark >= 60: return 'B'
    elif mark >= 50: return 'C+'
    elif mark >= 40: return 'C'
    elif mark >= 30: return 'D'
    return 'F'

def calculate_grade(mark):
    if mark >= 90: return 'A+'
    elif mark >= 80: return 'A'
    elif mark >= 70: return 'B+'
    elif mark >= 60: return 'B'
    elif mark >= 50: return 'C+'
    elif mark >= 40: return 'C'
    elif mark >= 30: return 'D'
    return 'F'

def home(request):
    total_students = Result.objects.values('exam_number').distinct().count()
    total_results = Result.objects.count()
    total_subjects = Subject.objects.count()
    avg_score = Result.objects.aggregate(avg=Avg('average_mark'))['avg'] or 0
    
    return render(request, 'home.html', {
        'total_students': total_students,
        'total_results': total_results,
        'total_subjects': total_subjects,
        'avg_score': round(avg_score, 2),
        'subjects_list': SUBJECTS_LIST  # <--- ADD THIS LINE
    })

def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'teacher_login.html')

def teacher_logout(request):
    logout(request)
    return redirect('home')

@login_required
def teacher_dashboard(request):
    results = Result.objects.all().order_by('-created_at')
    total_results = Result.objects.count()
    total_students = Result.objects.values('exam_number').distinct().count()
    avg_score = Result.objects.aggregate(avg=Avg('average_mark'))['avg'] or 0
    return render(request, 'dashboard.html', {
        'results': results,
        'total_results': total_results,
        'total_students': total_students,
        'avg_score': round(avg_score, 2)
    })

@login_required
def delete_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    result.delete()
    messages.success(request, f"Result for {result.student_name} deleted successfully.")
    return redirect('teacher_dashboard')
@login_required
def upload_result(request):
    if request.method == 'POST':
        form = ResultUploadForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            subject_names = request.POST.getlist('subject_name[]')
            subject_cas = request.POST.getlist('subject_ca[]')
            subject_exams = request.POST.getlist('subject_exam[]')

            subjects_data = []
            total_marks = 0
            count = 0
            
            for name, ca, exam in zip(subject_names, subject_cas, subject_exams):
                # Convert empty strings to 0.0
                ca_val = float(ca) if ca.strip() else 0.0
                exam_val = float(exam) if exam.strip() else 0.0
                
                # Only save if the teacher entered at least one score for this subject
                if ca_val > 0 or exam_val > 0:
                    total = ca_val + exam_val
                    if total > 100: total = 100 # Cap at 100 just in case
                    
                    subjects_data.append({
                        'subject_name': name.strip(),
                        'marks': total,
                        'grade': calculate_grade(total),
                    })
                    total_marks += total
                    count += 1

            if count == 0:
                messages.error(request, 'Please enter valid scores for at least one subject.')
                return render(request, 'upload_result.html', {'form': form, 'subjects': SUBJECTS_LIST})

            result.total_marks = total_marks
            result.average_mark = round(total_marks / count, 2)
            result.grade = calculate_grade(result.average_mark)
            result.save()
            
            for sd in subjects_data:
                Subject.objects.create(
                    result=result,
                    subject_name=sd['subject_name'],
                    marks=sd['marks'],
                    grade=sd['grade'],
                )
            messages.success(request, f"Result for {result.student_name} published successfully!")
            return redirect('teacher_dashboard')
    else:
        form = ResultUploadForm()
    
    return render(request, 'upload_result.html', {'form': form, 'subjects': SUBJECTS_LIST})

def student_check(request):
    if request.method == 'POST':
        form = StudentCheckForm(request.POST)
        if form.is_valid():
            try:
                result = Result.objects.get(
                    exam_number=form.cleaned_data['exam_number'].strip(),
                    student_name__iexact=form.cleaned_data['student_name'].strip(),
                    year=form.cleaned_data['year'],
                    term=form.cleaned_data['term'],
                )
                return render(request, 'result_view.html', {'result': result})
            except Result.DoesNotExist:
                return render(request, 'result_not_found.html', {'form': form})
    else:
        form = StudentCheckForm()
    return render(request, 'student_check.html', {'form': form})