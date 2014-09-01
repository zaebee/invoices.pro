#-*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import Invoice


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('owner', 'status') # User will be filled in by the view.
