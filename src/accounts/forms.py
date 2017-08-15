import re
from django import forms


class StudentUpdateForm(forms.Form):
    email = forms.EmailField(max_length=250)
    phone = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False

    class Meta:
        fields = ['email', 'phone', ]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        if not re.search('[0-9]', phone):
            raise forms.ValidationError(
                'Mobile phone number can not contain letters from alphabet')
        if len(phone) not in (10, 11):
            raise forms.ValidationError(
                'Mobile phone number must be 10 or 11 characters')
        return phone


class PasswordResetRequestForm(forms.Form):
    student_id = forms.CharField(label='Student ID',
                                 max_length=8,
                                 min_length=8)


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2
