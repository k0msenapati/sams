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
        "report/monthly/<int:student_id>/",
        views.monthly_attendance_report,
        name="monthly_report",
    ),
    path("report/monthly/", views.monthly_attendance_report, name="my_monthly_report"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
]
