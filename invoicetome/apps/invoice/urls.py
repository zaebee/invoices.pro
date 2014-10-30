from django.conf.urls import patterns, url, include
from invoice import views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'tasks', views.RecordViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)


urlpatterns += patterns('invoice.views',
    #Different views
    url(r'^generate/(?P<pk>[-_\d\w]+)/$', 'invoice_pdf', name='invoice_pdf'),
    url(r'^detail/(?P<uuid>[-_\d\w]+)/$', 'invoice_detail', name='invoice_detail'),
    url(r'^share/(?P<uuid>[-_\d\w]+)/$', 'invoice_share', name='invoice_share'),

)
