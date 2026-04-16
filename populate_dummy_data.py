# populate_dummy_data.py
import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
django.setup()

from core.models import User
from attendance.models import (
    Department, Section, Course, Professor, Student, 
    Lecture, Attendance
)

def create_dummy_data():
    print("Starting dummy data population...")

    # ==================== DEPARTMENTS ====================
    cse, _ = Department.objects.get_or_create(code="CSE", defaults={"name": "Computer Science and Engineering"})
    ece, _ = Department.objects.get_or_create(code="ECE", defaults={"name": "Electronics and Communication Engineering"})

    print(f"Departments created: {cse}, {ece}")

    # ==================== SECTIONS ====================
    section_cse, _ = Section.objects.get_or_create(
        department=cse, semester=5, name="A",
        defaults={"name": "A"}
    )
    section_ece, _ = Section.objects.get_or_create(
        department=ece, semester=5, name="A",
        defaults={"name": "A"}
    )

    # ==================== COURSES (Subjects) ====================
    courses = [
        # CSE Subjects
        {"code": "CS501", "name": "Database Management Systems", "dept": cse, "sem": 5},
        {"code": "CS502", "name": "Computer Networks", "dept": cse, "sem": 5},
        {"code": "CS503", "name": "Operating Systems", "dept": cse, "sem": 5},
        # ECE Subjects
        {"code": "EC501", "name": "Digital Signal Processing", "dept": ece, "sem": 5},
        {"code": "EC502", "name": "VLSI Design", "dept": ece, "sem": 5},
        {"code": "EC503", "name": "Communication Systems", "dept": ece, "sem": 5},
    ]

    course_objs = {}
    for c in courses:
        course, created = Course.objects.get_or_create(
            code=c["code"],
            department=c["dept"],
            semester=c["sem"],
            defaults={"name": c["name"], "credits": 4}
        )
        course_objs[c["code"]] = course
        print(f"Course created: {course}")

    # ==================== PROFESSORS ====================
    professors = []
    prof_data = [
        # CSE Professors
        ("prof_cse1", "Rahul", "Sharma", "CSE", "EMP001", "Assistant Professor"),
        ("prof_cse2", "Priya", "Das", "CSE", "EMP002", "Associate Professor"),
        ("prof_cse3", "Amit", "Kumar", "CSE", "EMP003", "Professor"),
        # ECE Professors
        ("prof_ece1", "Sanjay", "Patnaik", "ECE", "EMP004", "Assistant Professor"),
        ("prof_ece2", "Anjali", "Rao", "ECE", "EMP005", "Associate Professor"),
        ("prof_ece3", "Vikash", "Singh", "ECE", "EMP006", "Professor"),
    ]

    for username, first, last, dept_code, emp_id, designation in prof_data:
        dept = cse if dept_code == "CSE" else ece
        
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first,
                'last_name': last,
                'email': f"{username}@outr.ac.in",
                'role': 'professor',
                'is_staff': True,
            }
        )
        user.set_password('password123')
        user.save()

        prof, created = Professor.objects.get_or_create(
            user=user,
            defaults={
                'department': dept,
                'employee_id': emp_id,
                'designation': designation
            }
        )
        professors.append(prof)
        print(f"Professor created: {prof}")

    # ==================== STUDENTS ====================
    students = []
    student_data = []
    
    # 10 Students for CSE
    for i in range(1, 11):
        roll = f"2023CSE{str(i).zfill(3)}"
        student_data.append((f"student_cse{i}", f"Student{i}", "CSE", roll))
    
    # 10 Students for ECE
    for i in range(1, 11):
        roll = f"2023ECE{str(i).zfill(3)}"
        student_data.append((f"student_ece{i}", f"Student{i}", "ECE", roll))

    for username, name, dept_code, roll in student_data:
        dept = cse if dept_code == "CSE" else ece
        section = section_cse if dept_code == "CSE" else section_ece
        
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': name,
                'last_name': 'Kumar',
                'email': f"{username}@outr.ac.in",
                'role': 'student'
            }
        )
        user.set_password('password123')
        user.save()

        student, created = Student.objects.get_or_create(
            user=user,
            defaults={
                'roll_number': roll,
                'section': section,
                'admission_year': 2023
            }
        )
        students.append(student)
        print(f"Student created: {student.roll_number}")

    # ==================== SAMPLE ATTENDANCE ====================
    print("Creating sample attendance records...")

    today = date.today()
    
    # Create lectures for last 10 days for both departments
    for i in range(10):
        lecture_date = today - timedelta(days=i)
        
        # Create lectures for CSE subjects
        for course_code in ["CS501", "CS502", "CS503"]:
            course = course_objs[course_code]
            prof = random.choice([p for p in professors if p.department == cse])
            
            lecture, _ = Lecture.objects.get_or_create(
                course=course,
                section=section_cse,
                date=lecture_date,
                defaults={'professor': prof, 'topic': f"Topic for {course_code}"}
            )
            
            # Mark attendance for all students (70% present randomly)
            for student in [s for s in students if s.section == section_cse]:
                is_present = random.random() > 0.3  # 70% chance present
                Attendance.objects.get_or_create(
                    lecture=lecture,
                    student=student,
                    defaults={'is_present': is_present}
                )

        # Same for ECE
        for course_code in ["EC501", "EC502", "EC503"]:
            course = course_objs[course_code]
            prof = random.choice([p for p in professors if p.department == ece])
            
            lecture, _ = Lecture.objects.get_or_create(
                course=course,
                section=section_ece,
                date=lecture_date,
                defaults={'professor': prof, 'topic': f"Topic for {course_code}"}
            )
            
            for student in [s for s in students if s.section == section_ece]:
                is_present = random.random() > 0.3
                Attendance.objects.get_or_create(
                    lecture=lecture,
                    student=student,
                    defaults={'is_present': is_present}
                )

    print("\n🎉 Dummy data population completed successfully!")
    print("Login credentials:")
    print("Students & Professors → Username: student_cse1 / prof_cse1   Password: password123")
    print("Admin → Use your superuser (don't forget to set role = 'admin')")

if __name__ == "__main__":
    create_dummy_data()