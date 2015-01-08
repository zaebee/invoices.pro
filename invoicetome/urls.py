from django.conf.urls import patterns, include, url
from django.conf import settings

from django.views.generic import TemplateView, RedirectView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apps.local.views import RegistrationView, ActivationView, MainView
from apps.local.forms import CustomPasswordChangeForm, CustomSetPasswordForm


admin.autodiscover()

js_info_dict = {
    'packages': ('apps.invoice',),
}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^localeurl/', include('localeurl.urls')),
    url(r'^registration/register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^registration/activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^registration/', include('customregistration.urls')),
)

urlpatterns += patterns('invoice.views',
    url(r'^share/(?P<uuid>[-_\d\w]+)/$', 'invoice_share', name='invoice_share'),
)

urlpatterns += patterns('',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^jsi18n/null/$', 'django.views.i18n.null_javascript_catalog'),
)

urlpatterns += patterns('',
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'password_change_form': CustomPasswordChangeForm},
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='password_reset'),

    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'set_password_form': CustomSetPasswordForm},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
)

urlpatterns += patterns('',
    url(r'^$', MainView.as_view(), name='main-view'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
