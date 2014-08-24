from django.conf.urls import patterns, url

urlpatterns = patterns('invoice.views',
    #Different views
    url(r'^invoice/(?P<pk>[-_\d\w]+)/$', 'invoice_detail', name='invoice_detail'),

)
