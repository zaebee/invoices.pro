from django.contrib import admin

from .models import Invoice, Record, History

class TaskInlineAdmin(admin.TabularInline):
    model = Record
    extra = 0
    readonly_fields = ['description', 'quantity', 'unit_price', 'total']


class HistoryInlineAdmin(admin.TabularInline):
    model = History
    extra = 0
    readonly_fields = ['date_added', 'action', 'email']


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'uuid', 'owner', 'email', 'status', 'signed', 'date_added')
    list_filter = ('owner', 'status', 'signed')
    inlines = [TaskInlineAdmin, HistoryInlineAdmin]


admin.site.register(Invoice, InvoiceAdmin)
