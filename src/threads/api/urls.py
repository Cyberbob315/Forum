from django.conf.urls import url
from .views import ThreadSearchView, UserThreadAPIView

urlpatterns = [
    url(r'^search$', ThreadSearchView.as_view(), name='search'),
    url(r'^user$', UserThreadAPIView.as_view(), name='user_thread'),
]
