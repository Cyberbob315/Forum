from django import forms

class StudentUpdateForm(forms.Form):
    email = forms.EmailField(max_length=250)
    class Meta:
        fields = ['email']
