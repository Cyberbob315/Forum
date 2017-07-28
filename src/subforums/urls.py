from django.conf.urls import url
from .views import SubforumListView, subforum_detail, subforum_draft_list

app_name = 'forum'

urlpatterns = [
    url(r'^$', SubforumListView.as_view(), name='list'),
    url(r'^(?P<slug>[-\w]+)/$', subforum_detail, name='detail'),
    url(r'^(?P<slug>[-\w]+)/drafts/$', subforum_draft_list, name='drafts'),
]
