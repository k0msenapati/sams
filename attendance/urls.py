from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("professor/dashboard/", views.professor_dashboard, name="professor_dashboard"),
    path(
        "take-attendance/<int:course_id>/<int:section_id>/",
        views.take_attendance,
        name="take_attendance",
    ),
    path(
        "report/section/<int:course_id>/<int:section_id>/",
        views.section_attendance_report,
        name="section_report",
    ),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
]
