from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'website.views.index'),
    url(r'^about/$', 'website.views.about'),
    url(r'^sisters/$', 'website.views.sisters'),
    url(r'^philanthropy/$', 'website.views.philanthropy'),
    url(r'^social/$', 'website.views.social'),
    url(r'^recruitment/$', 'website.views.recruitment'),
    url(r'^parents/$', 'website.views.parents'),
    url(r'^alumnae/$', 'website.views.alumnae'),
    url(r'^contact/$', 'website.views.contact'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change.html', 'post_change_redirect': '/'}),
    url(r'^accounts/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'password_reset.html', 'email_template_name': 'password_reset_email.html'}),
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html', 'post_reset_redirect' : '/accounts/login/'}),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}),

    url(r'^sistersonly/$', 'website.views.sistersonly'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
