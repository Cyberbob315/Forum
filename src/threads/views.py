from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Thread


class ThreadDetailView(DetailView):
    model = Thread
    context_object_name = 'thread'
    template_name = 'threads/thread-detail.html'


def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    context_dict = {'thread': thread,
                    'is_liked':thread.likes.filter(student_id__exact=request.user.id).count() > 0
                    }
    return render(request, 'threads/thread-detail.html', context_dict)
