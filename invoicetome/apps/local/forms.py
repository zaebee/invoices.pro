# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail


class RegistrationForm(RegistrationFormUniqueEmail):

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                required=False,
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    def clean_username(self):
        """

        """
        if 'email' in self.data:
            self.cleaned_data['username'] = self.data['email']
        return self.cleaned_data['username']
