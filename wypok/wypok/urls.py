from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from allauth.account import views as allauth


urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),

    # allauth
    #url(r'^', include('allauth.urls')),
    url(r'^signup/$', allauth.signup, name='account_signup'),
    url(r'^login/$', allauth.login, name='account_login'),
    url(r'^logout/$', allauth.logout, name='account_logout'),

    # custom settings
    # todo: clean it up (maybe rewrite?)
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

    # profiles
    url(r'^users/', include('profiles.urls')),

    # tags
    url(r'^tags/', include('tags.urls')),

    # posts
    url(r'^posts/', include('posts.urls')),

    # comments
    url(r'^comments/', include('comments.urls')),

    # sections
    url(r'^', include('sections.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),

        # treat media as static files (disabled because docker takes care of this)
        # todo: remove completely?
        #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ]
