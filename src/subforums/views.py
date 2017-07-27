from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Subforum

THREADS_PER_PAGE = 7


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
    }
    return render(request, 'subforums/subforum-detail.html', context_dict)
