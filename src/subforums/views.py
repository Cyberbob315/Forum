from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Subforum


class SubforumListView(ListView):
    model = Subforum
    template_name = 'subforums/forum.html'
    context_object_name = 'subforum_list'


def subforum_detail(request, slug):
    subforum = get_object_or_404(Subforum, slug=slug)
    thread_list = subforum.threads.filter(
        published_date__isnull=False
    ).order_by(
        '-created_date'
    )
    context_dict = {
        'subforum': subforum,
        'thread_list': thread_list,
    }
    return render(request, 'subforums/subforum-detail.html', context_dict)
