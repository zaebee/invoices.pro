#-*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Invoice, Record, Header


class HeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Header


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record


class InvoiceSerializer(serializers.ModelSerializer):
    records = RecordSerializer(source='records', many=True, required=False)
    headers = HeaderSerializer(source='headers', required=False)

    class Meta:
        model = Invoice
        exclude = ('owner',)
