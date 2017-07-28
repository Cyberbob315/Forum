from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Subforum

THREADS_PER_PAGE = 7


class SubforumListView(ListView):
    model = Subforum
    template_name = 'subforums/forum.html'
    context_object_name = 'subforum_list'


@login_required(login_url=reverse_lazy('accounts:login'))
def subforum_draft_list(request, slug):
    if not request.user.is_superuser:
        return render(request, 'error.html')
    subforum = get_object_or_404(Subforum, slug=slug)
    thread_list = subforum.threads.filter(
        published_date__isnull=True
    ).order_by(
        '-created_date'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(thread_list, THREADS_PER_PAGE)
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.num_pages(paginator.num_pages)
    context_dict = {
        'subforum': subforum,
        'thread_list': threads,
        'is_draft': True
    }
    return render(request, 'subforums/subforum-detail.html', context_dict)


def subforum_detail(request, slug):
    subforum = get_object_or_404(Subforum, slug=slug)
    thread_list = subforum.threads.filter(
        published_date__isnull=False
    ).order_by(
        '-is_pinned',
        '-created_date'
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(thread_list, THREADS_PER_PAGE)
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.num_pages(paginator.num_pages)
    context_dict = {
        'subforum': subforum,
        'thread_list': threads,
        'is_draft': False
    }
    return render(request, 'subforums/subforum-detail.html', context_dict)
