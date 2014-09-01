# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, redirect
from django.utils import translation
from django.contrib.auth.models import User

from django.conf import settings

from .models import Invoice, Record


from .serializers import InvoiceSerializer, RecordSerializer

from rest_framework.decorators import detail_route
from rest_framework import viewsets



class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        #import ipdb;ipdb.set_trace()
        if self.request.user.is_anonymous():
            user, _ = User.objects.get_or_create(email=obj.email)
        else:
            user = self.request.user
        obj.owner = user

    def _create(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RecordViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    def _pre_save(self, obj):
        if self.request.user.is_anonymous():
            user, _ = User.objects.get_or_create(email=obj.email)
        else:
            user = self.request.user
        obj.owner = user
