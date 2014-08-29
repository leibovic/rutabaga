from django.conf.urls import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sisters/$', 'website.views.sisters'),
    url(r'^sisters/(\d+)/$', 'website.views.sisters_profile'),

    url(r'^sisters/profile/$', 'website.views.edit_profile'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change.html', 'post_change_redirect': '/accounts/change/done/'}),
    url(r'^accounts/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    url(r'^accounts/reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset.html', 'email_template_name': 'accounts/password_reset_email.html'}),
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset_confirm.html', 'post_reset_redirect' : '/accounts/login/'}),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),

    #url(r'^sistersonly/events/$', 'website.views.sistersonly_events'),
    #url(r'^sistersonly/events/(\d+)/$', 'website.views.sistersonly_events_attendance'),
    url(r'^sistersonly/attendance/$', 'website.views.sistersonly_attendance'),
    url(r'^sistersonly/directory/$', 'website.views.sistersonly_directory'),
    url(r'^sistersonly/feedback/$', 'website.views.sistersonly_feedback'),

    url(r'^sistersonly/elections/ois/$', 'website.views.sistersonly_elections_ois'),
    url(r'^sistersonly/elections/ois/results/$', 'website.views.sistersonly_elections_ois_results'),
    url(r'^sistersonly/elections/loi/$', 'website.views.sistersonly_elections_loi'),
    url(r'^sistersonly/elections/loi/results/$', 'website.views.sistersonly_elections_loi_results'),
    url(r'^sistersonly/elections/slating/$', 'website.views.sistersonly_elections_slating'),
    url(r'^sistersonly/elections/slating/results/$', 'website.views.sistersonly_elections_slating_results'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # For static media files served in a development environment
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
