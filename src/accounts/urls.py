from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (
    user_profile,
    user_profile_edit,
    update_profile,
    user_login,
    change_password,
    user_activity,
)
from .resetpass import ResetPasswordRequestView, PasswordResetConfirmView

app_name = 'accounts'

urlpatterns = [
    url(r'^login-site/', user_login, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^(?P<student_id>\d+)/password-change/$', change_password,
        name='password-change'),
    url(r'^(?P<student_id>\d+)/profile/$', user_profile, name='profile'),
    url(r'^(?P<student_id>\d+)/activity/$', user_activity, name='activity'),
    url(r'^(?P<student_id>\d+)/profile/edit/$', user_profile_edit,
        name='profile-edit'),
    url(r'^(?P<student_id>\d+)/profile/api/update-info/$', update_profile,
        name='profile-update'),
    url(r'^reset_password/$', ResetPasswordRequestView.as_view(),
        name='reset_password'),
    url(
        r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(), name='reset_password_confirm')
]
