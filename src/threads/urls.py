from django.conf.urls import url, include
from .views import post_thread, thread_detail_view, ThreadUpdateView
from .api import PostLikeToggleApi, CheckLikeApi, PublishThreadApi, DeleteThreadApi

app_name = 'threads'

urlpatterns = [
    url(r'^show/(?P<pk>\d+)/$', thread_detail_view, name='detail'),
    url(r'^show/(?P<pk>\d+)/like/$', PostLikeToggleApi.as_view(), name='like'),
    url(r'^show/(?P<pk>\d+)/check-like/$', CheckLikeApi.as_view(),
        name='check-like'),
    url(r'^(?P<pk>\d+)/edit/$', ThreadUpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/publish/$', PublishThreadApi.as_view(), name='publish'),
    url(r'^(?P<pk>\d+)/delete/$', DeleteThreadApi.as_view(), name='delete-api'),
    url(r'^create/$', post_thread, name='create'),
    url(r'^comments/', include('comments.urls', namespace='comments')),
]
