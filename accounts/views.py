from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models
import sections


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
    posts   = sections.models.Post.objects.filter(author=profile.user)

    return render(response, 'account/profile.html', {'profile': profile, 'posts': posts})
