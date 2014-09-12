from django.dispatch import Signal


# A new user has registered.
invoice_sended = Signal(providing_args=["invoice", "request"])
