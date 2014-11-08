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
    disabled = serializers.Field(source='_extra_fields.disabled')

    class Meta:
        model = Record

    def extra_fields(self, obj):
        request = self.context.get('request', None)
        if obj.invoice.owner == request.user and obj.invoice.status == obj.invoice.STATUS_DRAFT:
            disabled = False
        else:
            disabled = True
        data = {
            'disabled' : disabled
        }
        return data

    def to_native(self, obj):
        if obj:
            fields = self.extra_fields(obj)
            obj._extra_fields = fields
        return super(RecordSerializer, self).to_native(obj)


class InvoiceSerializer(serializers.ModelSerializer):
    records = RecordSerializer(source='records', many=True, required=False)
    headers = HeaderSerializer(source='headers', required=False)
    histories = HistorySerializer(source='histories', required=False, read_only=True)
    date_added = serializers.DateTimeField(read_only=True)
    recipient_email = serializers.EmailField(source="recipient_email", read_only=True)
    disabled = serializers.Field(source='_extra_fields.disabled')

    class Meta:
        model = Invoice
        exclude = ('owner',)

    def extra_fields(self, obj):
        request = self.context.get('request', None)
        if obj.owner == request.user and obj.status == obj.STATUS_DRAFT:
            disabled = False
        else:
            disabled = True
        data = {
            'disabled' : disabled
        }
        return data

    def to_native(self, obj):
        if obj:
            fields = self.extra_fields(obj)
            obj._extra_fields = fields
        return super(InvoiceSerializer, self).to_native(obj)
