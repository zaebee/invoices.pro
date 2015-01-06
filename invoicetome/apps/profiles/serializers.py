#-*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    #disabled = serializers.Field(source='_extra_fields.disabled')

    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_superuser', 'groups', 'date_joined',)
