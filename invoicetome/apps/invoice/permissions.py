# -*- coding: utf-8 -*-

from rest_framework import permissions


class IsInvoiceOwner(permissions.BasePermission):
    """
    Current invoice able to edit he's own model
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
