from django.conf.urls import url
from . import views

app_name = 'student_admin'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^subforum/(?P<slug>[-\w]+)/drafts/$', views.subforum_draft_list,
        name='drafts'),
    url(r'^user_list/$', views.user_list, name='user-list'),
]
