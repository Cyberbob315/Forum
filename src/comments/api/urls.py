from django.conf.urls import url
from .views import UserCommentAPIView

urlpatterns = [
    url(r'^user$', UserCommentAPIView.as_view(), name='user_comment'),
]
