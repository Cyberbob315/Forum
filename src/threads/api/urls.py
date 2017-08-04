from django.conf.urls import url
from .views import (
    ThreadSearchView,
    UserThreadAPIView,
    PostLikeToggleApi,
    CheckLikeApi,
    DeleteThreadApi,
    PublishThreadApi
)

urlpatterns = [
    url(r'^search$', ThreadSearchView.as_view(), name='search'),
    url(r'^user$', UserThreadAPIView.as_view(), name='user_thread'),
    url(r'^(?P<pk>\d+)/like/$', PostLikeToggleApi.as_view(),
        name='like-toggle'),
    url(r'^(?P<pk>\d+)/check-like/$', CheckLikeApi.as_view(),
        name='check-like'),
    url(r'^(?P<pk>\d+)/delete/$', DeleteThreadApi.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/publish/$', PublishThreadApi.as_view(), name='publish'),
]
