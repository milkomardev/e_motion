import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneNumberValidator:
    regex = re.compile(r'^\+\d{1,3}\d{7,12}$')
    message = ("Phone number must be in the format '+yyy xxxxxxxxx' with a country code of 1-3 digits and 7-12 digits "
               "for the phone number.")
    code = 'invalid_phone_number'

    def __call__(self, value):
        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code)