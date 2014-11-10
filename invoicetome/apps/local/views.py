# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login

from django.utils.translation import ugettext_lazy as _

from registration.backends.default.views import RegistrationView as BaseRegistrationView
from registration.backends.default.views import ActivationView as BaseActivationView

from local.forms import RegistrationForm


class RegistrationView(BaseRegistrationView):

    form_class = RegistrationForm


class ActivationView(BaseActivationView):

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        user.backend = 'local.backends.EmailOrUsernameModelBackend'
        login(request, user)
        messages.success(request, _('Your account was activated!'))
        return ('main-view', (), {})


class MainView(TemplateView):
    template_name = 'default.html'
