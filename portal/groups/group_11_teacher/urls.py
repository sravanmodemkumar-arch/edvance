"""Teacher portal URL config."""
from django.urls import path
from portal.groups.group_11_teacher.views import dashboard_view, attendance_view
from portal.groups.group_11_teacher.views import homework_view, results_view

app_name = "teacher"

urlpatterns = [
    path("", dashboard_view.TeacherDashboardView.as_view(), name="dashboard"),
    path("attendance/", attendance_view.AttendanceMarkView.as_view(), name="attendance"),
    path("homework/", homework_view.HomeworkView.as_view(), name="homework"),
    path("results/", results_view.ResultsView.as_view(), name="results"),
]
