from django import forms
from .models import Result

class ResultUploadForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['exam_number', 'student_name', 'student_photo', 'year', 'term', 'category', 'track', 'class_name', 'remarks']
        widgets = {
            'exam_number': forms.TextInput(attrs={'placeholder': 'e.g. BFC2024001'}),
            'student_name': forms.TextInput(attrs={'placeholder': "Student's full name"}),
            'year': forms.NumberInput(attrs={'min': 2000, 'max': 2099, 'placeholder': '2024'}),
            'term': forms.Select(),
            'category': forms.Select(attrs={'id': 'id_category', 'onchange': 'toggleTrack()'}),
            'track': forms.Select(attrs={'id': 'id_track'}),
            'class_name': forms.TextInput(attrs={'placeholder': 'e.g. JSS 1A or SSS 2B'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional remarks...'}),
        }

class StudentCheckForm(forms.Form):
    exam_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'e.g. BFC2024001'}))
    student_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Your full registered name'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 2000, 'max': 2099, 'placeholder': '2024'}))
    term = forms.ChoiceField(choices=[('', 'Select Term')] + Result.TERM_CHOICES, widget=forms.Select())