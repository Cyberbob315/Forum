from django import forms
from . import models


class CommentForm(forms.ModelForm):
    content = forms.Textarea()

    class Meta:
        model = models.Comment
        fields = [
            'content',
        ]
