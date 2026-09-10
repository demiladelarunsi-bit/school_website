from django.core.management.base import BaseCommand
from portal.models import Result, Subject
from django.core.management.base import BaseCommand
from portal.models import Result, Subject

def calc_grade(mark):
    if mark >= 90: return 'A+'
    elif mark >= 80: return 'A'
    elif mark >= 70: return 'B+'
    elif mark >= 60: return 'B'
    elif mark >= 50: return 'C+'
    elif mark >= 40: return 'C'
    elif mark >= 30: return 'D'
    return 'F'

class Command(BaseCommand):
    help = 'Seed sample student results.'

    def handle(self, *args, **options):
        Result.objects.all().delete()

        samples = [
            {'exam_number': 'SCH2024001', 'student_name': 'Aarav Sharma', 'year': 2024, 'term': 'First', 'category': 'Senior', 'class_name': 'SS 2A', 'remarks': 'Excellent.',
             'subjects': [('Mathematics', 95), ('English Language', 88), ('Physics', 92), ('Chemistry', 85), ('Biology', 90)]},
            {'exam_number': 'SCH2024002', 'student_name': 'Diya Patel', 'year': 2024, 'term': 'First', 'category': 'Junior', 'class_name': 'JSS 1B', 'remarks': 'Good effort.',
             'subjects': [('Mathematics', 71), ('English Language', 81), ('Basic Science', 78), ('Social Studies', 85), ('Civic Education', 76)]},
        ]

        for data in samples:
            r = Result.objects.create(
                exam_number=data['exam_number'], student_name=data['student_name'],
                year=data['year'], term=data['term'], category=data['category'], class_name=data['class_name'], remarks=data['remarks'],
            )
            total = 0
            for name, marks in data['subjects']:
                Subject.objects.create(result=r, subject_name=name, marks=marks, grade=calc_grade(marks))
                total += marks
            r.total_marks = total
            r.average_mark = round(total / len(data['subjects']), 2)
            r.grade = calc_grade(r.average_mark)
            r.save()

        self.stdout.write(self.style.SUCCESS(f'\n✓ Seeded {len(samples)} sample results!'))