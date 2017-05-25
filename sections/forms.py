from django import forms

from sections.models import Section


class SectionCreateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'description',)


class SectionUpdateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('description',)


class SectionDeleteForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ()
