#-*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Invoice, Record, Header, History


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        exclude = ('invoice',)


class HeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Header
        exclude = ('invoice',)


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record


class InvoiceSerializer(serializers.ModelSerializer):
    records = RecordSerializer(source='records', many=True, required=False)
    headers = HeaderSerializer(source='headers', required=False)
    histories = HistorySerializer(source='histories', required=False, read_only=True)
    date_added = serializers.DateTimeField(read_only=True)
    recipient_email = serializers.EmailField(source="recipient_email", read_only=True)

    class Meta:
        model = Invoice
        exclude = ('owner',)
        #ordering_fields = ('id',)
        #ordering = '-id'
