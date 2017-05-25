from django import forms

from comments.models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ()
