from django.contrib.sites.models import Site
from django.conf import settings

HELLOSIGN_CLIENT_ID = getattr(settings, 'HELLOSIGN_CLIENT_ID', '')
HELLOSIGN_API_KEY = getattr(settings, 'HELLOSIGN_API_KEY', '')


def common(request):

    return {
        'HELLOSIGN_CLIENT_ID': HELLOSIGN_CLIENT_ID,
        'HELLOSIGN_API_KEY': HELLOSIGN_API_KEY,
    }
