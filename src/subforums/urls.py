from django.conf.urls import url
from .views import SubforumListView,subforum_detail

app_name = 'forum'

urlpatterns = [
    url(r'^$', SubforumListView.as_view(), name='list'),
    url(r'^(?P<slug>[-\w]+)/$',subforum_detail, name='detail'),
]
