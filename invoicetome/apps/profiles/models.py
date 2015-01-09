# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from json_field import JSONField


class StripeProfile(models.Model):
    user = models.ForeignKey(User, related_name='stripe_profiles')
    access_token = models.CharField(_('Access Token'), max_length=200, blank=True, null=True)
    stripe_user_id = models.CharField(_('Stripe User ID'), max_length=200, blank=True, null=True)
    stripe_publishable_key = models.CharField(_('Stripe Publishable Key'), max_length=200, blank=True, null=True)
    refresh_token = models.CharField(_('Refresh Token'), max_length=200, blank=True, null=True)
    json_data = JSONField(_('JSON data'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    enabled = models.BooleanField(_('Enabled'), default=True)

    class Meta:
        verbose_name = _('Stripe Profile')
        verbose_name_plural = _('Stripe Profiles')
        ordering = ('-created_at',)

    def __unicode__(self):
        return "%s: %s" % (self.access_token, self.user)

