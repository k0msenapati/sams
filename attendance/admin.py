from django.contrib import admin
from .models import Department, Section, Course, Professor, Student, Lecture, Attendance


# ====================== BASIC MODELS ======================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "hod")
    search_fields = ("code", "name")
    list_filter = ("code",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("department", "semester", "name")
    list_filter = ("department", "semester")
    search_fields = ("department__code", "name")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "semester", "credits")
    list_filter = ("department", "semester")
    search_fields = ("code", "name")


# ====================== FACULTY & STUDENTS ======================
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "employee_id", "designation")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "employee_id",
    )
    list_filter = ("department",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "user", "section", "admission_year")
    search_fields = (
        "roll_number",
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    list_filter = ("section__department", "section__semester", "admission_year")
    raw_id_fields = ("user", "section")


# ====================== ATTENDANCE MODELS ======================
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("course", "section", "date", "professor", "topic")
    list_filter = ("course__department", "section__semester", "date")
    search_fields = ("course__code", "course__name", "topic")
    date_hierarchy = "date"
    raw_id_fields = ("professor",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("lecture", "student", "is_present", "marked_at")
    list_filter = ("is_present", "lecture__date", "lecture__course")
    search_fields = ("student__roll_number", "student__user__first_name")
    raw_id_fields = ("lecture", "student")
