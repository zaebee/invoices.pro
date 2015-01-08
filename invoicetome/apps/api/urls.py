from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from invoice import views as invoice_views
from profiles import views as profiles_views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'invoices', invoice_views.InvoiceViewSet)
router.register(r'tasks', invoice_views.RecordViewSet)
router.register(r'users', profiles_views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

urlpatterns += patterns('invoice.views',
    #Different views
    url(r'^pdf/(?P<uuid>[-_\d\w]+)/$', 'invoice_pdf', name='invoice_pdf'),
    url(r'^sign/(?P<uuid>[-_\d\w]+)/$', 'invoice_sign', name='invoice_sign'),
    url(r'^hellosign_callback/$', 'hellosign_callback', name='hellosign_callback'),
    url(r'^stripe_callback/$', 'stripe_callback', name='stripe_callback'),
)
