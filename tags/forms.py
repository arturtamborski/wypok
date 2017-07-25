from django import forms

from tags.models import Tag


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'description')


class TagUpdateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'description')


class TagDeleteForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ()
