#-*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import StripeProfile


class StripeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeProfile
        exclude = ('json_data',)


class UserSerializer(serializers.ModelSerializer):
    #disabled = serializers.Field(source='_extra_fields.disabled')
    stripes = StripeProfileSerializer(source='stripe_profiles', many=True, required=False)

    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_superuser', 'groups', 'date_joined',)
