from django.views.generic import ListView
from braces.views import LoginRequiredMixin
from .models import Mark


class SubjectListView(LoginRequiredMixin, ListView):
    template_name = 'subjects/transcript.html'
    context_object_name = 'mark_list'
    login_url = '/accounts/login-site'
    model = Mark

    def get_queryset(self):
        return Mark.objects.filter(student=self.request.user).order_by('year')
