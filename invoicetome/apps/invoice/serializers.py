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
    date_added = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Invoice
        exclude = ('owner',)
