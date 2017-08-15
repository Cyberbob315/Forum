from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from accounts.api.views import (
    UserListAPIView,
    StudentProfileViewset,
    ResetPasswordToDefault,
)

router = DefaultRouter()
router.register('', StudentProfileViewset, base_name='account')

urlpatterns = [
    url(r'^user_list/$', UserListAPIView.as_view(), name='user_list'),
    url(r'^reset_pass/$', ResetPasswordToDefault.as_view(), name='reset_pass'),
]
