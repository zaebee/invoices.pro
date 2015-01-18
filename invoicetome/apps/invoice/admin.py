from django.contrib import admin

from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'uuid', 'owner', 'email', 'status', 'signed', 'date_added')
    list_filter = ('owner', 'status')


admin.site.register(Invoice, InvoiceAdmin)
