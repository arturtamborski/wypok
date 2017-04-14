from django.shortcuts import render
from django.urls import reverse

def home(response):
    return render(response, 'home/home.html')
