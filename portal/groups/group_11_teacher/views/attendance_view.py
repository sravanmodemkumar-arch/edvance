"""Teacher attendance marking — HTMX row-level updates."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AttendanceMarkView(LoginRequiredMixin, TemplateView):
    template_name = "group_11_teacher/attendance.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Mark Attendance"
        ctx["breadcrumbs"] = [
            {"label": "Dashboard", "url": "teacher:dashboard"},
            {"label": "Attendance", "url": None},
        ]
        return ctx
