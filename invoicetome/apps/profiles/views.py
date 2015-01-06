# -*- coding: utf-8 -*-

import os

from annoying.functions import get_object_or_None

from django import http
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
