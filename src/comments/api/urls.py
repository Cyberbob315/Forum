from django.conf.urls import url
from .views import UserCommentAPIView, DeleteCommentAPIView

urlpatterns = [
    url(r'^user$', UserCommentAPIView.as_view(), name='user_comment'),
    url(r'^(?P<pk>\d+)/delete$', DeleteCommentAPIView.as_view(), name='delete'),
]
