from django.conf.urls import url
from .views import SubjectListView

app_name = 'student'

urlpatterns = [
    url(r'^transcript/$', SubjectListView.as_view(), name='transcript'),
]
