from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include('allauth.urls')),
    url(r'^', include('home.urls')),
]
