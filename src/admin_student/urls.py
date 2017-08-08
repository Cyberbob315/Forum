from django.conf.urls import url
from . import views

app_name = 'student_admin'

urlpatterns = [
    url(r'^subforum/(?P<slug>[-\w]+)/drafts/$', views.subforum_draft_list,
        name='drafts'),
    url(r'', views.user_list, name='user-list'),
]
