from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from wypok.utils.membership_required import membership_required
from wypok.utils.ownership_required import ownership_required
from notifications.models import Notification
from notifications.forms import NotificationCreateForm
