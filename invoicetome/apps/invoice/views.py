# -*- coding: utf-8 -*-

import os
import uuid
import json
import hashlib, hmac

from hellosign_sdk import HSClient
from hellosign_sdk.utils import NotFound, Gone
from rauth import OAuth2Service

from annoying.functions import get_object_or_None

from django import http
from django.conf import settings
from django.utils import translation
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Invoice, Record
from . import signals
from .serializers import InvoiceSerializer, RecordSerializer
from .permissions import IsInvoiceOwner


HELLOSIGN_CLIENT_ID = getattr(settings, 'HELLOSIGN_CLIENT_ID', '')
HELLOSIGN_API_KEY = getattr(settings, 'HELLOSIGN_API_KEY', '')
HELLOSIGN_TEST_MODE = getattr(settings, 'HELLOSIGN_TEST_MODE', True)
HELLOSIGN_PRESIGN_DIR = getattr(settings, 'HELLOSIGN_PRESIGN_DIR', '/tmp')
STRIPE_CLIENT_ID = getattr(settings, 'STRIPE_CLIENT_ID', '')
STRIPE_CLIENT_SECRET = getattr(settings, 'STRIPE_CLIENT_SECRET', '')


stripe_connect_service = OAuth2Service(
    name = 'stripe',
    client_id = STRIPE_CLIENT_ID,
    client_secret = STRIPE_CLIENT_SECRET,
    authorize_url = 'https://connect.stripe.com/oauth/authorize',
    access_token_url = 'https://connect.stripe.com/oauth/token',
    base_url = 'https://api.stripe.com/',
)


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
        user = self.request.user
        if not obj.owner and user.is_authenticated():
            obj.owner = user

    def post_save(self, obj, *args, **kwargs):
        """
        Send invoice via email
        """
        recipient_email = self.request.DATA.get('recipient_email', None)
        recieved = self.request.DATA.get('recieved', False)
        if recipient_email != obj.recipient_email:
            obj.recipient_email = recipient_email
            signals.invoice_sent.send(sender=self.__class__,
                                        invoice=obj,
                                        request=self.request)
        if recipient_email and recieved:
            signals.invoice_recieved.send(sender=self.__class__,
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
    filename = '%s/%s' % (HELLOSIGN_PRESIGN_DIR, filename)
    fields = [
        [
            {
                "api_id": "uniqueIdHere_2",
                "name": "",
                "type": "signature",
                "x": 450,
                "y": 310,
                "width": 240,
                "height": 60,
                "required": True,
                "signer": 0
            }
        ]
    ]

    if os.path.exists(filename):
        response = client.send_signature_request_embedded(
            test_mode=HELLOSIGN_TEST_MODE,
            client_id=HELLOSIGN_CLIENT_ID,
            title=invoice.uuid,
            signers=[
                {
                    'email_address': invoice.email,
                    'name': invoice.company_name,
                }
            ],
            form_fields_per_document=json.dumps(fields),
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


@api_view(['POST'])
def hellosign_callback(request):
    response = 'Hello API Event Received'
    hash_match = False
    event_type = event_time = ''
    try:
        json_event_data = request.DATA.get('json')
        data = json.loads(json_event_data)
        event_time = data['event']['event_time']
        event_type = data['event']['event_type']
        event_time = data['event']['event_time']
        event_hash = data['event']['event_hash']
        invoice_uid = data['signature_request']['title']
        print data
        hash_match = event_hash == hmac.new(
            HELLOSIGN_API_KEY,
            (event_time + event_type),
            hashlib.sha256).hexdigest()
        invoice = get_object_or_None(Invoice, uuid=invoice_uid)
    except:
        print 'Hellosign API Callback ERROR'


    if hash_match and invoice:
        signals.invoice_signature_called.send(sender=None,
                                    invoice=invoice,
                                    request=request,
                                    signature_event=event_type)
    return Response(response, content_type="application/json")



@api_view(['GET'])
def stripe_callback(request):
    # the temporary code returned from stripe
    user = request.user
    if user.is_anonymous():
        return Response({'error': 'User is not authorized'}, status=403)

    code = request.GET.get('code', False)
    error = request.GET.get('error', False)

    # identify what we are going to ask for from stripe
    data = {
        'grant_type': 'authorization_code',
        'code': code
    }

    if not code:
        return Response({'error': 'empty code'}, status=403)

    # Get the access_token using the code provided
    resp = stripe_connect_service.get_raw_access_token(method='POST', data=data)

    # process the returned json object from stripe
    stripe_payload = json.loads(resp.text)
    if stripe_payload.get('error'):
        messages.success(request, stripe_payload.get('error_description'), 'alert')
        return redirect('main-view')
    profile, _ = user.stripe_profiles.get_or_create(
        stripe_user_id=stripe_payload['stripe_user_id']
    )
    #connect stripe profile to our user
    profile.access_token = stripe_payload['access_token']
    profile.stripe_publishable_key = stripe_payload['stripe_publishable_key']
    profile.refresh_token = stripe_payload['refresh_token']
    profile.json_data = stripe_payload
    profile.save()
    messages.success(request, 'Stripe successfully Connected!')

    # Sample return of the access_token, please don't do this! this is
    # just an example that it does in fact return the access_token
    return redirect('main-view')


def stripe_connect(request):
    params = {'response_type': 'code'}
    url = stripe_connect_service.get_authorize_url(**params)
    return redirect(url)
