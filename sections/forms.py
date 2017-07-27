from django import forms

from sections.models import Section


class SectionCreateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'description', 'background')


class SectionUpdateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('description', 'background')


class SectionDeleteForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ()
