from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from braces.views._access import LoginRequiredMixin
from .models import Comment
from . import forms
from threads.models import Thread


class CommentCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'comments/comment-create.html'
    model = Comment
    form_class = forms.CommentForm

    login_url = '/accounts/login-site'

    def form_valid(self, form):
        comment = form.save(commit=False)
        thread_id = self.kwargs.get('pk')
        try:
            thread = Thread.objects.get(pk=thread_id)
        except:
            return render(self.request, 'error_404.html')
        comment.thread = thread
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('threads:detail', kwargs={'pk': self.object.thread.pk})

    def get_context_data(self, **kwargs):
        try:
            thread = Thread.objects.get(pk=self.kwargs.get('pk'))
        except:
            return render(self.request, 'error_404.html')
        kwargs['thread'] = thread
        return super().get_context_data(**kwargs)
