from django.conf.urls import patterns, url, include
from invoice import views
from rest_framework.routers import DefaultRouter


urlpatterns = patterns('invoice.views',
    #Different views
    url(r'^invoice/$', 'invoice_list', name='invoice_list'),
    url(r'^invoice/(?P<pk>[-_\d\w]+)/$', 'invoice_detail', name='invoice_detail'),

)


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'tasks', views.RecordViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
