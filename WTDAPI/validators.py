from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_characters(value):
    if not re.match('^[a-zA-Z0-9_& .-]+$', value):
        raise ValidationError(
            _('Field contains disallowed characters'))

def check_negative_number(value):
    if value < 0:
        raise ValidationError(
            _('Field cannot be a negative value'))

def check_negative_number(value):
    if value < 0:
        raise ValidationError(
            _('Field cannot be a negative value'))

def check_zero_number(value):
    if value == 0:
        raise ValidationError(
            _('Field cannot be a zero value'))