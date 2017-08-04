from django import forms
import bleach
from django.conf import settings

from . import models


class CommentForm(forms.ModelForm):
    content = forms.Textarea()

    class Meta:
        model = models.Comment
        fields = [
            'content',
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        cleaned_content = bleach.clean(text=content,
                                       tags=settings.BLEACH_VALID_TAGS,
                                       attributes=settings.BLEACH_VALID_ATTRS,
                                       styles=settings.BLEACH_VALID_STYLES,
                                       protocols=bleach.ALLOWED_PROTOCOLS + ['data'])
        return cleaned_content
