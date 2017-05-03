from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models


#class ProfileList(generic.ListView):
#    queryset            = models.Account.objects.all()
#    template_name       = 'account/profile.html'
#    context_object_name = 'profiles'
#
#
#class ProfileDetail(generic.DetailView):
#    model               = models.Account
#    template_name       = 'blog/article.html'
#    context_object_name = 'profiles'

def profile(response, profile):
    profile = get_object_or_404(models.Profile.objects, user__username=profile)
    return render(response, 'account/profile.html', {'profile': profile})
