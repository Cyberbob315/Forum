from django.conf.urls import url
from django.conf.urls import include
from . import views

app_name = 'subforum-api'

urlpatterns = [
    url(r'^list/$', views.SubforumListAPIView.as_view(), name='list'),
]
