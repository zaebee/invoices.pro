from django.dispatch import Signal


# A new user has registered.
invoice_sended = Signal(providing_args=["invoice", "request"])
invoice_signature_called = Signal(providing_args=["invoice", "request", "signature_event"])
