from braces.views._access import SuperuserRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.db.models import Q

from accounts.models import StudentProfile
from subjects.models import Subject, Mark
from subforums.models import Subforum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

ITEMS_PER_PAGE = 7


@login_required(login_url='/accounts/login-site/')
def index(request):
    return render(request, 'admin_student/admin_base.html', {})


class SubjectListView(SuperuserRequiredMixin, ListView):
    template_name = 'admin_student/subject.html'
    login_url = '/accounts/login-site'
    model = Subject
    context_object_name = 'subject_list'

    def get_queryset(self):
        subjects = Subject.objects.all()
        query = self.request.GET.get('query')
        if query:
            subjects = subjects.filter(
                Q(subject_id__icontains=query) |
                Q(title__icontains=query)
            )
        page = self.request.GET.get('page', 1)
        paginator = Paginator(subjects, ITEMS_PER_PAGE)
        try:
            subject_list = paginator.page(page)
        except PageNotAnInteger:
            subject_list = paginator.page(1)
        except EmptyPage:
            subject_list = paginator.num_pages(paginator.num_pages)
        return subject_list


class MarkListView(SuperuserRequiredMixin, ListView):
    template_name = 'admin_student/transcript.html'
    login_url = 'accounts/login-site'
    model = Mark
    context_object_name = 'mark_list'

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        queryset = Mark.objects.filter(
            student__student_id=student_id
        ).order_by('year')
        return queryset

    def get_context_data(self, **kwargs):
        student_id = self.kwargs.get('student_id')
        subject_list = Subject.objects.exclude(
            mark__student__student_id=student_id
        ).order_by('title')
        kwargs['subject_list'] = subject_list
        kwargs['student'] = get_object_or_404(StudentProfile,
                                              student_id=student_id)
        return super().get_context_data(**kwargs)


class UserListView(SuperuserRequiredMixin, ListView):
    template_name = 'admin_student/user_list.html'
    login_url = 'accounts/login-site'
    model = StudentProfile
    context_object_name = 'student_list'

    def get_queryset(self):
        queryset = StudentProfile.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(private_email__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(student_id__icontains=search_query)
            )
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, ITEMS_PER_PAGE)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.num_pages(paginator.num_pages)
        return users


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
    paginator = Paginator(thread_list, ITEMS_PER_PAGE)
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
