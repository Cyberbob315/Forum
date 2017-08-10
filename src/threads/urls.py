from django.conf.urls import url, include
from .views import (
    post_thread,
    thread_detail_view,
    ThreadUpdateView,
    pin_thread
)

app_name = 'threads'

urlpatterns = [
    url(r'^show/(?P<pk>\d+)/$', thread_detail_view, name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', ThreadUpdateView.as_view(), name='edit'),
    url(r'^(?P<thread_id>\d+)/pin/$', pin_thread, name='pin'),
    url(r'^create/$', post_thread, name='create'),
    url(r'^comments/', include('comments.urls', namespace='comments')),
]
