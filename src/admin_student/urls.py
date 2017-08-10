from django.conf.urls import url

from . import views

app_name = 'student_admin'

urlpatterns = [
    url(r'^subforum/(?P<slug>[-\w]+)/drafts/$', views.subforum_draft_list,
        name='drafts'),
    url(r'^index/$', views.UserListView.as_view(), name='user-list'),
    url(r'^subject/$', views.SubjectListView.as_view(), name='subject-list'),
    url(r'^user/(?P<student_id>\d+)/transcript/$',
        views.MarkListView.as_view(), name='transcript'),
]
