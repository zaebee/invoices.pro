"""Template tags for Invoices"""

from random import sample
from urllib import urlencode
from datetime import datetime

from django.template import Library

from random import sample

from invoice.models import Invoice


register = Library()


@register.inclusion_tag('tags/dummy.html')
def get_my_invoices(user, template='tags/my_invoices.html'):
    """Return the my invoices"""
    return {
        'template': template,
        'items': Invoice.objects.filter(owner=user).order_by('-date_added')
    }

