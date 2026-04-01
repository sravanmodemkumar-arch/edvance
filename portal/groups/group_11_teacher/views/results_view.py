"""Teacher results and grading view."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ResultsView(LoginRequiredMixin, TemplateView):
    template_name = "group_11_teacher/results.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Results & Grading"
        ctx["breadcrumbs"] = [
            {"label": "Dashboard", "url": "teacher:dashboard"},
            {"label": "Results", "url": None},
        ]
        return ctx
