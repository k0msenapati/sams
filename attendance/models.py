from django.db import models
from core.models import User

# ====================== UNIVERSITY STRUCTURE ======================
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    hod = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True, related_name='hod_dept')

    def __str__(self):
        return f"{self.code} - {self.name}"


class Section(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sections')
    semester = models.PositiveIntegerField(choices=[(i, f'Semester {i}') for i in range(1, 9)])
    name = models.CharField(max_length=10)

    class Meta:
        unique_together = ('department', 'semester', 'name')
        ordering = ['department', 'semester', 'name']

    def __str__(self):
        return f"{self.department.code} Sem-{self.semester} {self.name}"


class Course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    semester = models.PositiveIntegerField(choices=[(i, f'Semester {i}') for i in range(1, 9)])
    credits = models.PositiveIntegerField(default=4)

    class Meta:
        unique_together = ('code', 'department', 'semester')

    def __str__(self):
        return f"{self.code} - {self.name}"


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'professor'})
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professors')
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Prof. {self.user.get_full_name() or self.user.username}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    roll_number = models.CharField(max_length=20, unique=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='students')
    admission_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name() or self.user.username}"


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lectures')
    date = models.DateField()
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, related_name='lectures_conducted')
    topic = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'section', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.course.code} | {self.section} | {self.date}"


class Attendance(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    is_present = models.BooleanField(default=False)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lecture', 'student')

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.roll_number} - {status}"