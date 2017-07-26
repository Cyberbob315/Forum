from django.conf.urls import url
from .views import ThreadDetailView
from .api import PostLikeToggleApi

app_name = 'threads'

urlpatterns = [
    url(r'^show/(?P<pk>\d+)/$', ThreadDetailView.as_view(), name='detail'),
    url(r'^show/(?P<pk>\d+)/like/$', PostLikeToggleApi.as_view(), name='like'),
]
