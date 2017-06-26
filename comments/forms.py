from django import forms
from django.core.exceptions import ValidationError

from comments.models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'attachment',)

    def clean(self):
        cleaned = super().clean()
        content = cleaned['content']
        attachment = cleaned['attachment']

        if not len(content) and not attachment:
            raise ValidationError('You need to provide at least text or attachment')


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'attachment',)

    def clean(self):
        cleaned = super().clean()
        content = cleaned['content']
        attachment = cleaned['attachment']

        if not len(content) and not attachment:
            raise ValidationError('You need to provide at least text or attachment')


class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ()
