from django.forms.utils import ErrorList
from django import forms


class UserOwnerMixin(object):
    def form_valid(self, form):
        if self.request.user.is_superuser or form.instance.author == self.request.user:
            return super(UserOwnerMixin, self).form_valid(form)
        form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(
            ['This user is not allowed to change this data'])
        return self.form_invalid(form)
