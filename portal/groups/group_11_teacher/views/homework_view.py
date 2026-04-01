"""Teacher homework assignment view."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeworkView(LoginRequiredMixin, TemplateView):
    template_name = "group_11_teacher/homework.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Homework"
        ctx["breadcrumbs"] = [
            {"label": "Dashboard", "url": "teacher:dashboard"},
            {"label": "Homework", "url": None},
        ]
        return ctx
