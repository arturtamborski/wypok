from django.shortcuts import render
from django.urls import reverse

def home(response):
    return render(response, 'account/home.html')
