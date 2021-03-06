from django import forms

from profiles.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'description', 'avatar',)


class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ()
