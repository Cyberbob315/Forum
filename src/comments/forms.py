from django import forms
import bleach
from django.conf import settings

from . import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'style': 'min-height:500px;background-color:white;padding:15px',
                    'class': 'editable medium-editor-textarea'}
            )
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        cleaned_content = bleach.clean(text=content,
                                       tags=settings.BLEACH_VALID_TAGS,
                                       attributes=settings.BLEACH_VALID_ATTRS,
                                       styles=settings.BLEACH_VALID_STYLES,
                                       protocols=bleach.ALLOWED_PROTOCOLS + [
                                           'data'])
        return cleaned_content
