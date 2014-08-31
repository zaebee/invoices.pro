# -*- coding: utf-8 -*-
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#from transmeta import TransMeta


class Invoice(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SAVED = 'saved'
    STATUS_SENDED = 'sended'
    STATUS_RECIEVED = 'recieved'

    STATUS_CHOICES = {
        STATUS_DRAFT: _("Draft"),
        STATUS_SAVED: _("Saved"),
        STATUS_SENDED: _("Sended"),
        STATUS_RECIEVED: _("Recieved"),
    }

    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='created_invoices')
    recipient = models.ForeignKey(User, verbose_name=_('Recipient'), related_name='sended_invoices', blank=True, null=True)

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

    subtotal = models.DecimalField(_('Subtotal Price'), decimal_places=2, max_digits=20)
    tax = models.DecimalField(_('Sales Tax %'), decimal_places=2, max_digits=6, default=0)
    total = models.DecimalField(_('Total Price'), decimal_places=2, max_digits=20, editable=False)

    date_added = models.DateTimeField(_(u'Date Added'), auto_now_add=True)
    records = models.ForeignKey('Record', verbose_name=_('Records'), related_name='records', null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES.items(), default=STATUS_DRAFT)

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s - #%s" % (seldf.email, self.invoice_uid)

    @models.permalink
    def get_absolute_url(self):
        return ('invoice_detail', None, {'pk': self.id})


class Record(models.Model):
    description = models.TextField(_('Description'))
    quantity = models.PositiveIntegerField(_('Quantity'))
    unit_price = models.DecimalField(_('Unit Price'), decimal_places=2, max_digits=20)
    total = models.DecimalField(_('Total'), decimal_places=2, max_digits=20)
