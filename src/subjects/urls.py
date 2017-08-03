from django.conf.urls import url
from .views import SubjectListView

urlpatterns = [
    url(r'^transcript/$', SubjectListView.as_view(), name='transcript'),
]
