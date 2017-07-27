from django.conf.urls import url
from .views import post_thread, thread_detail_view
from .api import PostLikeToggleApi, CheckLikeApi

app_name = 'threads'

urlpatterns = [
    url(r'^show/(?P<pk>\d+)/$', thread_detail_view, name='detail'),
    url(r'^show/(?P<pk>\d+)/like/$', PostLikeToggleApi.as_view(), name='like'),
    url(r'^show/(?P<pk>\d+)/check-like/$', CheckLikeApi.as_view(),
        name='check-like'),
    url(r'^create/$', post_thread, name='create'),
]
