from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from .utils import send_reset_password_email
from django.views.generic import FormView
from .forms import PasswordResetRequestForm, SetPasswordForm
from .models import StudentProfile


class ResetPasswordRequestView(FormView):
    template_name = 'accounts/forgot_pass.html'
    success_url = '/accounts/login-site/'
    form_class = PasswordResetRequestForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'error_404.html')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'error_404.html')
        messages.error(request, '')
        form = self.form_class(request.POST)
        if not form.is_valid():
            messages.error(request, 'Invalid Input')
            return self.form_invalid(form)
        student_id = form.cleaned_data.get('student_id')
        users = StudentProfile.objects.filter(student_id=student_id)
        if not users.exists():
            messages.error(request,
                           'This username does not exist in the system.')
            return self.form_invalid(form)
        user = users[0]
        if not user.private_email:
            messages.error(request,
                           'This user did not register any private email')
            return self.form_invalid(form)
        send_reset_password_email(receiver=user)
        return render(request, 'accounts/email_sended.html',
                      {'email': user.private_email})
        return self.form_valid(form)


class PasswordResetConfirmView(FormView):
    template_name = 'accounts/forgot_pass.html'
    success_url = '/accounts/login-site'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = StudentProfile.objects.get(pk=uid)
        except (
                TypeError, ValueError, OverflowError,
                StudentProfile.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user,
                                                        token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request,
                               'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,
                           'The reset password link is no longer valid.')
            return self.form_invalid(form)
