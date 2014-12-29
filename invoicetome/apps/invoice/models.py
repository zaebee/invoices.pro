# -*- coding: utf-8 -*-
import os
import uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from templated_email import send_templated_mail

from . import signals

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@invoiceto.me')
BASE_PDF_DIR = '/tmp'


class Invoice(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SAVED = 'saved'
    STATUS_SENT = 'sent'
    STATUS_RECIEVED = 'recieved'

    STATUS_CHOICES = {
        STATUS_DRAFT: _("Draft"),
        STATUS_SAVED: _("Saved"),
        STATUS_SENT: _("Sent"),
        STATUS_RECIEVED: _("Recieved"),
    }

    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='created_invoices')
    recipient_email = models.CharField(_('Recipient Email'), max_length=255, blank=True, null=True)

    company_name = models.CharField(_('Company Name'), max_length=255)
    address = models.CharField(_('Address'), max_length=255)
    city = models.CharField(_('City'), max_length=255)
    address_second = models.CharField(_('Address'), max_length=255, null=True, blank=True)

    phone = models.CharField(_('Phone'), max_length=255)
    email = models.EmailField(_('Email'))

    invoice_name = models.CharField(_('Invoice Name'), max_length=255)
    invoice_uid = models.CharField(_('Invoice Uid'), max_length=255)
    invoice_po = models.CharField(_('Invoice PO'), max_length=255)

    client_name = models.CharField(_('Client Name'), max_length=255)
    client_company = models.CharField(_('Client Company'), max_length=255)

    notes_top = models.TextField(_('Notes Top'), null=True, blank=True)
    notes_bottom = models.TextField(_('Notes Bottom'), null=True, blank=True)

    subtotal = models.DecimalField(_('Subtotal Price'),
                                   decimal_places=2, max_digits=20)
    tax = models.DecimalField(_('Sales Tax %'),
                              decimal_places=2, max_digits=6, default=0)
    total = models.DecimalField(_('Total Price'),
                                decimal_places=2, max_digits=20)

    date_added = models.DateTimeField(_(u'Date Added'), auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES.items(),
                              default=STATUS_DRAFT)
    uuid = models.CharField(_('Uuid'), max_length=255, blank=True, null=True)
    signature_request_id = models.CharField(_('Signature Request ID'), max_length=255, blank=True, null=True)
    signature_id = models.CharField(_('Signature ID'), max_length=255, blank=True, null=True)
    signed = models.BooleanField(_('Signed'), default=False)

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ('-date_added',)

    def __unicode__(self):
        return "%s - #%s" % (self.email, self.invoice_uid)

    @models.permalink
    def get_absolute_url(self):
        return ('invoice_share', None, {'uuid': self.uuid})

    @property
    def get_signature_request_file(self):
        filename = '%s/%s.pdf' % (BASE_PDF_DIR, self.uuid)
        if self.signature_request_id:
            created = client.get_signature_request_file(
                self.signature_request_id,
                filename)
            if created:
                return filename
        return False

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(Invoice, self).save(*args, **kwargs)


class Record(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name=_('Invoice'),
                                related_name='records', null=True, blank=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    quantity = models.PositiveIntegerField(_('Quantity'))
    unit_price = models.DecimalField(_('Unit Price'), decimal_places=2, max_digits=20)
    total = models.DecimalField(_('Total'), decimal_places=2, max_digits=20)

    def __unicode__(self):
        return self.description


class Header(models.Model):
    invoice = models.OneToOneField(Invoice, verbose_name=_('Invoice'),
                                   related_name='headers', null=True, blank=True)
    h_description = models.CharField(_('Description'), max_length=255)
    h_quantity = models.CharField(_('Quantity'), max_length=255)
    h_unit_price = models.CharField(_('Unit Price'), max_length=255)
    h_total = models.CharField(_('Total'), max_length=255)
    subtotal = models.CharField(_('Subtotal'), max_length=255)
    tax = models.CharField(_('Tax'), max_length=255)
    total = models.CharField(_('Total'), max_length=255)

    def __unicode__(self):
        return self.h_description


class History(models.Model):
    ACTION_CREATED = 'created'
    ACTION_SENT = 'sent'
    ACTION_RECIEVED = 'recieved'
    ACTION_DECLINED = 'declined'

    ACTION_CHOICES = {
        ACTION_CREATED: _('Created'),
        ACTION_SENT: _('Sent to email'),
        ACTION_RECIEVED: _('Recieved from email'),
        ACTION_DECLINED: _('Declined'),
    }
    invoice = models.ForeignKey(Invoice, verbose_name=_('Invoice'),
                                   related_name='histories', null=True, blank=True)
    email = models.CharField(_('Email'), max_length=255)
    action = models.CharField(max_length=255, choices=ACTION_CHOICES.items(),
                              default=ACTION_CREATED)
    date_added = models.DateTimeField(_(u'Date Added'), auto_now_add=True)

    def __unicode__(self):
        return self.action


def send_invoice(sender, invoice, request, **kwargs):
    invoice.status = Invoice.STATUS_SENT
    data = {
        'invoice': invoice
    }
    send_templated_mail('invoice', DEFAULT_FROM_EMAIL, [invoice.recipient_email], data)
    invoice.date_added = datetime.now()
    invoice.save()
    History.objects.create(invoice=invoice, action=History.ACTION_SENT, email=invoice.recipient_email)


def create_history_log(sender, instance, created, **kwargs):
    if created:
        History.objects.create(invoice=instance, action=History.ACTION_CREATED)


signals.invoice_sended.connect(send_invoice)

models.signals.post_save.connect(create_history_log, sender=Invoice)
