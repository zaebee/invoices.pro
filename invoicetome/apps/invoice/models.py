# -*- coding: utf-8 -*-
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#from transmeta import TransMeta


class Invoice(models.Model):
    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='invoices')

    company_name = models.CharField(_('Company Name'), max_length=255)
    address = models.CharField(_('Address'), max_length=255)
    city = models.CharField(_('City'), max_length=255)
    address_second = models.CharField(_('Address'), max_length=255, null=True, blank=True)

    phone = models.CharField(_('Phone'), max_length=255)
    email = models.EmailField(_('Email'))

    invoice_name = models.CharField(_('Invoice Name'), max_length=255)
    invoice_uid = models.PositiveIntegerField(_('Invoice Uid'))
    invoice_po = models.PositiveIntegerField(_('Invoice PO'))

    client_name = models.CharField(_('Client Name'), max_length=255)
    client_company = models.CharField(_('Client Company'), max_length=255)

    notes_top = models.CharField(_('Notes Top'), max_length=255, null=True, blank=True)
    notes_bottom = models.CharField(_('Notes Bottom'), max_length=255, null=True, blank=True)

    subtotal = models.DecimalField(_(u'Subtotal Price'), decimal_places=2, max_digits=20)
    tax = models.DecimalField(_('Sales Tax %'), decimal_places=2, max_digits=6, default=0)
    total = models.DecimalField(_('Total Price'), decimal_places=2, max_digits=20, editable=False)

    date_added = models.DateTimeField(_(u'Date Added'), auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s - #%s" % (seldf.email, self.invoice_uid)

    @models.permalink
    def get_absolute_url(self):
        return ('invoice_detail', None, {'pk': self.id})
