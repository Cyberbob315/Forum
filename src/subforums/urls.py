from django.conf.urls import url
from .views import SubforumListView

app_name = 'subforums'

urlpatterns = [
    url(r'^$', SubforumListView.as_view(), name='list'),
]
