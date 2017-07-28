from django.conf.urls import url
from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^(?P<pk>\d+)/add/$', views.CommentCreate.as_view(),
        name='post-comment'),
]
