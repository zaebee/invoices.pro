# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login

from django.utils.translation import ugettext_lazy as _

from registration.views import ActivationView as BaseActivationView
from registration.backends.default.views import RegistrationView as BaseRegistrationView

from local.forms import RegistrationForm


class RegistrationView(BaseRegistrationView):

    form_class = RegistrationForm

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        password = request.POST.get('password1')
        new_user = authenticate(username=user.email,
                                password=password)
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        messages.success(request, _('Your account was created! You need confirm email address.'))
        return ('main-view', (), {})


class MainView(TemplateView):
    template_name = 'default.html'
