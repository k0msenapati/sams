from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Section, Course, Professor, Student, Lecture, Attendance


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "professor":
        return redirect("professor_dashboard")
    elif request.user.role == "student":
        return redirect("student_dashboard")
    elif request.user.role == "admin":
        return redirect("/admin/")

    return redirect("login")


@login_required
def professor_dashboard(request):
    if request.user.role != "professor":
        messages.error(request, "Access denied!")
        return redirect("home")

    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        messages.error(request, "Professor profile not found.")
        return redirect("home")

    # Get courses taught by this professor (for now, show all from department)
    courses = Course.objects.filter(department=professor.department)

    context = {
        "professor": professor,
        "courses": courses,
        "today": timezone.now().date(),
    }
    return render(request, "attendance/professor_dashboard.html", context)


@login_required
def take_attendance(request, course_id, section_id):
    if request.user.role != "professor":
        messages.error(request, "Only professors can take attendance.")
        return redirect("home")

    professor = get_object_or_404(Professor, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    section = get_object_or_404(Section, id=section_id)

    # Get all students in this section
    students = Student.objects.filter(section=section).order_by("roll_number")

    # Today's date (or allow selecting date later)
    today = timezone.now().date()

    # Check if lecture already exists for today
    lecture, created = Lecture.objects.get_or_create(
        course=course, section=section, date=today, defaults={"professor": professor}
    )

    if request.method == "POST":
        for student in students:
            is_present = request.POST.get(f"present_{student.id}") == "on"  # type: ignore
            Attendance.objects.update_or_create(
                lecture=lecture, student=student, defaults={"is_present": is_present}
            )
        messages.success(request, f"Attendance for {course.code} saved successfully!")
        return redirect("professor_dashboard")

    existing_present_ids = [
        att.student_id  # type: ignore
        for att in Attendance.objects.filter(lecture=lecture, is_present=True)
    ]

    context = {
        "course": course,
        "section": section,
        "students": students,
        "lecture": lecture,
        "existing_present_ids": existing_present_ids,
        "today": today,
    }
    return render(request, "attendance/take_attendance.html", context)


@login_required
def section_attendance_report(request, course_id, section_id):
    if request.user.role != "professor":
        messages.error(request, "Only professors can access this.")
        return redirect("professor_dashboard")

    professor = get_object_or_404(Professor, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    section = get_object_or_404(Section, id=section_id)

    # Get all students in this section
    students = Student.objects.filter(section=section).order_by("roll_number")

    today = timezone.now().date()
    current_year = today.year

    report_data = []

    for student in students:
        # Get attendance for this student in this course
        attendances = Attendance.objects.filter(
            student=student, lecture__course=course, lecture__date__year=current_year
        )

        total_classes = attendances.count()
        present = attendances.filter(is_present=True).count()

        effective_total = min(total_classes, 30)
        percentage = (
            round((present / effective_total * 100), 2) if effective_total > 0 else 0
        )
        eligible = percentage >= 75

        report_data.append(
            {
                "student": student,
                "total_classes": total_classes,
                "present": present,
                "effective_total": effective_total,
                "percentage": percentage,
                "eligible": eligible,
            }
        )

    # Overall section summary
    total_lectures = Lecture.objects.filter(
        course=course, section=section, date__year=current_year
    ).count()
    effective_lectures = min(total_lectures, 30)

    context = {
        "course": course,
        "section": section,
        "report_data": report_data,
        "total_lectures": total_lectures,
        "effective_lectures": effective_lectures,
        "professor": professor,
    }

    return render(request, "attendance/section_report.html", context)


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        messages.error(request, "Access denied!")
        return redirect("home")

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect("home")

    today = timezone.now().date()
    current_year = today.year

    # Get all attendances for this student
    attendances = Attendance.objects.filter(
        student=student, lecture__date__year=current_year
    ).select_related("lecture__course")

    from collections import defaultdict

    report = defaultdict(
        lambda: {
            "course_code": "",
            "course_name": "",
            "total_classes": 0,
            "present": 0,
            "monthly": defaultdict(lambda: {"total": 0, "present": 0}),
        }
    )

    for att in attendances:
        course_id = att.lecture.course.id  # type: ignore
        month_key = att.lecture.date.strftime("%Y-%m")

        if not report[course_id]["course_code"]:
            report[course_id]["course_code"] = att.lecture.course.code
            report[course_id]["course_name"] = att.lecture.course.name

        report[course_id]["total_classes"] += 1
        if att.is_present:
            report[course_id]["present"] += 1

        # Monthly data
        report[course_id]["monthly"][month_key]["total"] += 1
        if att.is_present:
            report[course_id]["monthly"][month_key]["present"] += 1

    # Calculate percentages with 30-class cap
    final_report = []
    overall_present = 0
    overall_total = 0

    for data in report.values():
        total = data["total_classes"]
        present = data["present"]

        effective_total = min(total, 30)
        percentage = (
            round((present / effective_total * 100), 2) if effective_total > 0 else 0
        )
        eligible = percentage >= 75

        data["effective_total"] = effective_total
        data["percentage"] = percentage
        data["eligible"] = eligible

        final_report.append(data)

        overall_present += present
        overall_total += effective_total

    overall_percentage = (
        round((overall_present / overall_total * 100), 2) if overall_total > 0 else 0
    )
    overall_eligible = overall_percentage >= 75

    context = {
        "student": student,
        "report": final_report,
        "overall_percentage": overall_percentage,
        "overall_eligible": overall_eligible,
        "current_year": current_year,
    }

    return render(request, "attendance/student_dashboard.html", context)
