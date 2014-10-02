# -*- coding: utf-8 -*-

import pdfcrowd
import uuid
#import xhtml2pdf.pisa as pisa
#import cStringIO as StringIO

from django import http
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.conf import settings

from rest_framework.decorators import detail_route
from rest_framework import viewsets
from rest_framework import permissions

from .models import Invoice, Record
from . import signals
from .serializers import InvoiceSerializer, RecordSerializer
from .permissions import IsInvoiceOwner



class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsInvoiceOwner,)
    filter_fields = ('status', 'recipient_email')

    def get_queryset(self):
        """
        This view should return a list of all the invoices
        for the currently authenticated user.
        """
        status = self.request.QUERY_PARAMS.get('status')
        user = self.request.user
        if user.is_anonymous():
            qs = Invoice.objects.none()
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


@login_required
def _invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice.objects.filter(owner=request.user), pk=pk)
    data = {
        'invoice': invoice
    }
    html = render_to_string('detail.html', data)

    if request.POST:
        result = StringIO.StringIO()
        pdf = pisa.CreatePDF(StringIO.StringIO(html.encode('utf8')),
                             result)

        if not pdf.err:
            return http.HttpResponse(
                result.getvalue(),
                mimetype='application/pdf')

    return render(request, '', {})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.filter(owner=request.user), pk=pk)
    data = {
        'invoice': invoice
    }
    return render(request, 'detail.html', data)


def invoice_share(request, uuid):
    invoice = get_object_or_404(Invoice, uuid=uuid)
    data = {
        'invoice': invoice,
        'share': True
    }
    return render(request, 'detail.html', data)


@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice.objects.filter(owner=request.user), pk=pk)
    data = {
        'invoice': invoice
    }
    html = render_to_string('detail.html', data)

    try:
        # create an API client instance
        client = pdfcrowd.Client("zaebee", "04483d20d43af67d661b0656154f71c3")

        # convert a web page and store the generated PDF to a variable
        pdf = client.convertHtml(html.encode('utf8'))

         # set HTTP response headers
        response = http.HttpResponse(mimetype="application/pdf")
        response["Cache-Control"] = "max-age=0"
        response["Accept-Ranges"] = "none"
        response["Content-Disposition"] = "attachment; filename=invoiceto.me.pdf"

        # send the generated PDF
        response.write(pdf)
    except pdfcrowd.Error, why:
        response = http.HttpResponse(mimetype="text/plain")
        response.write(why)
    return response
