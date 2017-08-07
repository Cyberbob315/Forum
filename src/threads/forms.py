from django import forms
import bleach
from django.conf import settings
from .models import Thread, ThreadImages


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('title', 'subforum', 'content',)
        widgets = {'content': forms.Textarea(
            attrs={'style': 'min-height:500px',
                   'class': 'editable medium-editor-textarea'})
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        cleaned_content = bleach.clean(text=content,
                                       tags=settings.BLEACH_VALID_TAGS,
                                       attributes=settings.BLEACH_VALID_ATTRS,
                                       styles=settings.BLEACH_VALID_STYLES,
                                       protocols=settings.BLEACH_VALID_PROTOCOLS)
        return cleaned_content

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        cleaned_title = bleach.clean(text=title,
                                     tags=settings.BLEACH_VALID_TAGS,
                                     attributes=settings.BLEACH_VALID_ATTRS,
                                     styles=settings.BLEACH_VALID_STYLES,
                                     protocols=settings.BLEACH_VALID_PROTOCOLS)
        return cleaned_title


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='image')

    class Meta:
        model = ThreadImages
        fields = ('image',)
