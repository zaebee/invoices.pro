# -*- coding: utf-8 -*-

import os
import uuid
import json

from hellosign_sdk import HSClient
from hellosign_sdk.utils import NotFound, Gone

from django import http
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.db.models import Q

from rest_framework.decorators import detail_route
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from .models import Invoice, Record
from . import signals
from .serializers import InvoiceSerializer, RecordSerializer
from .permissions import IsInvoiceOwner


HELLOSIGN_CLIENT_ID = getattr(settings, 'HELLOSIGN_CLIENT_ID', '')
HELLOSIGN_API_KEY = getattr(settings, 'HELLOSIGN_API_KEY', '')
HELLOSIGN_TEST_MODE = getattr(settings, 'HELLOSIGN_TEST_MODE', True)
BASE_PDF_DIR = '/tmp'


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    filter_fields = ('status', 'recipient_email')
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsInvoiceOwner,)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    lookup_field = 'uuid'
    ordering = ('-date_added',)

    def get_queryset(self):
        """
        This view should return a list of all the invoices
        for the currently authenticated user.
        """
        status = self.request.QUERY_PARAMS.get('status')
        recipient_email = self.request.QUERY_PARAMS.get('recipient_email')
        user = self.request.user
        if user.is_anonymous():
            qs = Invoice.objects.none()
        else:
            if recipient_email == user.email:
                qs = Invoice.objects.filter(recipient_email=user.email)
            else:
                qs = Invoice.objects.filter(owner=user)
        return qs

    def pre_save(self, obj):
        """
        Set request.user as  owner for new invoice
        or create new user by email
        """
        if self.request.user.is_anonymous():
            user, created = User.objects.get_or_create(email=obj.email, username=obj.email)
            if created:
                user.set_password(obj.email)
                user.save()
        else:
            user = self.request.user
        obj.owner = user

    def post_save(self, obj, *args, **kwargs):
        """
        Send invoice via email
        """
        recipient_email = self.request.DATA.get('recipient_email', None)
        if recipient_email != obj.recipient_email:
            obj.recipient_email = recipient_email
            signals.invoice_sended.send(sender=self.__class__,
                                        invoice=obj,
                                        request=self.request)


class RecordViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    def _pre_save(self, obj):
        if self.request.user.is_anonymous():
            user, _ = User.objects.get_or_create(email=obj.email)
        else:
            user = self.request.user
        obj.owner = user


def invoice_share(request, uuid):
    invoice = get_object_or_404(Invoice, uuid=uuid)
    data = {
        'invoice': invoice,
        'share': True
    }
    return render(request, 'detail.html', data)


def invoice_pdf(request, uuid):
    invoice = get_object_or_404(Invoice, uuid=uuid)
    path = invoice.get_signature_request_file
    with open(path, "rb") as f:
        data = f.read()
    response = http.HttpResponse(data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoiceto.me.pdf"'
    return response


def invoice_sign(request, uuid):
    invoice = get_object_or_404(Invoice, uuid=uuid)
    client = HSClient(api_key=HELLOSIGN_API_KEY)
    try:
        response = client.get_signature_request('%s' % invoice.signature_request_id)
        client.cancel_signature_request(invoice.signature_request_id)
    except (NotFound, Gone):
        pass
    filename = request.POST.get('filename', invoice.uuid)
    filename = '%s/%s' % (BASE_PDF_DIR, filename)
    if os.path.exists(filename):
        response = client.send_signature_request_embedded(
            test_mode=HELLOSIGN_TEST_MODE,
            client_id=HELLOSIGN_CLIENT_ID,
            title=invoice.uuid,
            signers=[
                {
                    'email_address': invoice.email,
                    'name': invoice.company_name
                }
            ],
            files=[filename]
        )
        invoice.signature_request_id = response.signature_request_id
    else:
        return http.HttpResponse(json.dumps({'sign_url': False}), content_type="application/json")
    signature = response.signatures[0]
    invoice.signature_id = signature.signature_id
    invoice.save()
    data = client.get_embedded_object(signature.signature_id)

    return http.HttpResponse(json.dumps(data.json_data), content_type="application/json")
