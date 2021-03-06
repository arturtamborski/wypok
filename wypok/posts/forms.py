from django import forms

from posts.models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'link', 'content', 'attachment',)


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'link', 'content', 'attachment',)


class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ()
