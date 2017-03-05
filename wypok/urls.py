from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^update/', views.update),
    url(r'^admin/', admin.site.urls),
]
