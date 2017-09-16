from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from allauth.account import views as allauth
from profiles import views as profiles

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # custom allauth urls
    #url(r'^', include('allauth.urls')),
    url(r'^signup/$', allauth.signup, name='account_signup'),
    url(r'^login/$', allauth.login, name='account_login'),
    url(r'^logout/$', allauth.logout, name='account_logout'),

    url(r'^settings/', include([
        url(r'^password/change/$',
            allauth.password_change, name='account_change_password'),
        url(r'^password/reset/$',
            allauth.password_reset, name='account_reset_password'),
        url(r'^password/reset/done/$',
            allauth.password_reset_done, name='account_reset_password_done'),
        url(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
            allauth.password_reset_from_key, name='account_reset_password_from_key'),
        url(r'^password/reset/key/done/$',
            allauth.password_reset_from_key_done, name='account_reset_password_from_key_done'),
        url(r'^email/confirm/$',
            allauth.email_verification_sent, name='account_verification_sent'),
        url(r'^email/confirm/(?P<key>[-:\w]+)/$',
            allauth.confirm_email, name='account_confirm_email'),
    ])),

    url(r'^user/', include('profiles.urls')),
    url(r'^tag/', include('tags.urls')),
    #url(r'^p/', include('posts.urls')),
    #url(r'^c/', include('comments.urls')),
    url(r'^', include('sections.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
