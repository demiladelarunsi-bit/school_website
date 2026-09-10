from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Result(models.Model):
    TERM_CHOICES = [('First', 'First Term'), ('Second', 'Second Term'), ('Third', 'Third Term')]
    GRADE_CHOICES = [('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'), ('C+', 'C+'), ('C', 'C'), ('D', 'D'), ('F', 'F')]
    CATEGORY_CHOICES = [('Junior', 'Junior Secondary'), ('Senior', 'Senior Secondary')]

    exam_number = models.CharField(max_length=20)
    student_name = models.CharField(max_length=120)
    year = models.IntegerField()
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Senior')
    class_name = models.CharField(max_length=60)
    total_marks = models.FloatField(default=0)
    average_mark = models.FloatField(default=0)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, default='F')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam_number', 'year', 'term')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_name} — {self.exam_number}"

class Subject(models.Model):
    result = models.ForeignKey(Result, related_name='subjects', on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)
    marks = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.subject_name}: {self.marks}"