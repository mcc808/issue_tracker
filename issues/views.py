from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Issue


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do_status = Status.objects.get(name="to do")
        in_p_status = Status.objects.get(name="in progress")
        done_status = Status.objects.get(name="done")
        team = self.request.user.team
        try:
            context["to_do_issues"] = Issue.objects.filter(
                team=team).filter(
                status=to_do_status).order_by("created on").reverse()
            context["in_p_issues"] = Issue.objects.filter(
                team=team
            ).filter(status=in_p_status).order_by("created_on").reverse
            context["done_issues"] = Issue.objects.filter(
                team=team
            ).filter(status=done_status).order_by("created_on").reverse()
        except Exception:
            context["to_do_issues"] = []
            context["in_p_issues"] = []
            context["done_issues"] = []
        return get_context_data
            

class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = "issues/detail.html"
    model = Issue

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issue/edit.html"
    model = Issue
    fields = [
        "title", "summary", "description", "assignee", "status"
    ]

    def test_func(self):
        issue = self.get_object()
        author = issue.author
        return author == self.request.user

class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = [
        "title", "summary", "description", "author", "assignee", "status"
    ]

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("issue_list")


    def test_func(self):
        issue = self.get_object()
        author = issue.author
        return author == self.request.user