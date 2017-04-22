from django.shortcuts import render
from django.urls import reverse

def profile(response, profile):
    return render(response, 'accounts/profile.html')
