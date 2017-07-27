from django import forms
from .models import Thread, ThreadImages


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('title', 'subforum', 'content',)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='image')

    class Meta:
        model = ThreadImages
        fields = ('image',)
