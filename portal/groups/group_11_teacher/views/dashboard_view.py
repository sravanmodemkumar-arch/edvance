"""Teacher dashboard — today's schedule, attendance summary, pending homework."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "group_11_teacher/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Teacher Dashboard"
        ctx["breadcrumbs"] = [{"label": "Dashboard", "url": None}]
        return ctx
