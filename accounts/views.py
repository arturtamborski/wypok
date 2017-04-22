from django.shortcuts import render
from django.urls import reverse

def home(response):
    return render(response, 'accounts/home.html')

def profile(response, profile):
    return render(response, 'accounts/profile.html')
