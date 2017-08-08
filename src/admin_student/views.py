from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from threads.models import Thread
from subforums.models import Subforum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

THREADS_PER_PAGE = 7

@login_required(login_url='/accounts/login-site/')
def index(request):
    return render(request, 'admin_student/admin_base.html', {})


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
    return render(request, 'admin_student/forum.html', context_dict)


@login_required(login_url='/accounts/login-site/')
def user_list(request):
    if request.user.is_superuser:
        return render(request, 'admin_student/user_list.html', {})
    return render(request, 'error.html', {})
