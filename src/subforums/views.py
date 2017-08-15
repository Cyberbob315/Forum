from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from subforums.utils import calculate_thread_rank
from .models import Subforum

THREADS_PER_PAGE = 10


class SubforumListView(ListView):
    model = Subforum
    template_name = 'subforums/forum.html'
    context_object_name = 'subforum_list'




def sort_thread_list(thread_queryset):
    new_list = [
        (thread, calculate_thread_rank(thread)) for thread in thread_queryset
    ]
    new_list.sort(key=lambda x: float(x[1]), reverse=True)
    return [thread[0] for thread in new_list]


def subforum_detail(request, slug):
    try:
        subforum = Subforum.objects.get(slug=slug)
    except:
        return render(request, 'error_404.html')
    thread_list = subforum.threads.filter(
        published_date__isnull=False
    )
    thread_list = sort_thread_list(thread_list)
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
