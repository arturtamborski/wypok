from django import forms

from . import models


class TagCreate(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ('name', 'description', 'background')


class TagUpdate(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ('name', 'description', 'background')


class TagDelete(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ()
