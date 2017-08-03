from django import forms
import bleach
from django.conf import settings
from .models import Thread, ThreadImages


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('title', 'subforum', 'content',)

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        cleaned_content = bleach.clean(content, settings.BLEACH_VALID_TAGS,
                                       settings.BLEACH_VALID_ATTRS,
                                       settings.BLEACH_VALID_STYLES)
        return cleaned_content

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        cleaned_title = bleach.clean(title, settings.BLEACH_VALID_TAGS,
                                       settings.BLEACH_VALID_ATTRS,
                                       settings.BLEACH_VALID_STYLES)
        return cleaned_title


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='image')

    class Meta:
        model = ThreadImages
        fields = ('image',)
