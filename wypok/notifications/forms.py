from django import forms

from notifications.models import Notification


class NotificationCreateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ()


class NotificationUpdateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ()


class NotificationDeleteForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ()
