from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

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

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change.html', 'post_change_redirect': '/accounts/change/done/'}),
    url(r'^accounts/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    url(r'^accounts/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset.html', 'email_template_name': 'accounts/password_reset_email.html'}),
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset_confirm.html', 'post_reset_redirect' : '/accounts/login/'}),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),

    url(r'^sistersonly/$', 'website.views.sistersonly'),
    url(r'^sistersonly/directory/$', 'website.views.sistersonly_directory'),
    url(r'^sistersonly/directory/(\d+)/$', 'website.views.sistersonly_profile'),
    url(r'^sistersonly/house/$', 'website.views.sistersonly_house'),
    url(r'^sistersonly/finance/$', 'website.views.sistersonly_finance'),
    url(r'^sistersonly/recruitment/$', 'website.views.sistersonly_recruitment'),
    url(r'^sistersonly/communications/$', 'website.views.sistersonly_communications'),
    url(r'^sistersonly/elections/$', 'website.views.sistersonly_elections'),
    url(r'^sistersonly/resources/$', 'website.views.sistersonly_resources'),

    url(r'^sistersonly/events/$', 'website.views.sistersonly_events'),
    url(r'^sistersonly/events/(\d+)/$', 'website.views.sistersonly_events_attendance'),

    url(r'^sistersonly/feedback/$', 'website.views.sistersonly_feedback'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # For static media files served in a development environment
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
)
