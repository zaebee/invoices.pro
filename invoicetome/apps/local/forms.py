# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

from registration.forms import RegistrationFormUniqueEmail


def validate_password_strength(value):
    """Validates that a password is as least 8 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 8

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must container at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must container at least 1 letter.'))


class RegistrationForm(RegistrationFormUniqueEmail):

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                required=False,
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].validators.append(validate_password_strength)

    def clean_username(self):
        if 'email' in self.data:
            self.cleaned_data['username'] = self.data['email']
        return self.cleaned_data['username']


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].validators.append(validate_password_strength)


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].validators.append(validate_password_strength)
