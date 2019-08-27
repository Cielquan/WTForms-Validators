from decimal import Decimal

try:
    from flask_babelex import _, ngettext as _n
except ImportError:
    def _(s): return s

    def _n(singular, plural, n):
        if n == 1:
            return singular
        return plural

from wtforms.compat import string_types as str_types
from wtforms.validators import StopValidation, ValidationError


class DecimalDigits(object):
    """
    Validates that a number has a minimum and/or maximum amount of decimal digits.

    Only numbers of type `int`, `float` and `decimal` are supported.

    :param min:
        The minimum required amount of decimal digits. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum amount of decimal digits. If not provided, maximum
        value will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `{min}` and `{max}` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """
    def __init__(self, min=-1, max=-1, message=None):
        assert min != -1 or max != -1, 'At least one of `min` or `max` must be specified.'
        assert max == -1 or min <= max, '`min` cannot be more than `max`.'
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        data = field.data
        if not isinstance(data, (int, float, Decimal)):
            raise ValidationError(_(u"""Data type "{type}" is not a supported.""").format(type=str(type(data))))
        s = str(data)
        digits = 0 if '.' not in s else len(s) - s.index('.') - 1

        if digits < self.min or self.max != -1 and digits > self.max:
            message = self.message
            if message is None:
                if self.max == -1:
                    message = _n(u'Number must have at least {min} decimal digit.',
                                 u'Number must have at least {min} decimal digits.',
                                 self.min)
                elif self.min == -1:
                    message = _n(u'Number can have at most {max} decimal digit.',
                                 u'Number can have at most {max} decimal digits.',
                                 self.max)
                elif self.min == self.max:
                    message = _n(u'Number must have exactly {max} decimal digit.',
                                 u'Number must have exactly {max} decimal digits.',
                                 self.max)
                else:
                    message = _(u'Number must have between {min} and {max} decimal digits.')

            raise ValidationError(message.format(field_name=field.label.text, min=self.min, max=self.max))


class EqualStateTo(object):
    """
    Compares the states of two fields.

    Checks if both field have the same state, like two checkboxes are checked or two inputs are filled.

    :param other_field_name:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `{field_name}` and `{other_field_name}` if desired.
    """
    def __init__(self, other_field_name, message=None):
        self.other_field_name = other_field_name
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.other_field_name]
        except KeyError:
            raise ValidationError(_(u"Invalid field name '{field_name}'.").format(field_name=self.other_field_name))

        other_field_empty = False
        if not other.raw_data or isinstance(other.raw_data[0], str_types) and not other.raw_data[0].strip():
            other_field_empty = True

        field_empty = False
        if not field.raw_data or isinstance(field.raw_data[0], str_types) and not field.raw_data[0].strip():
            field_empty = True

        if field_empty != other_field_empty:

            message = self.message
            if message is None:
                message = _(u"'{field_name}' and '{other_field_name}' must be of equal state.")

            field.errors[:] = []
            raise ValidationError(message.format(field_name=field.label.text, other_field_name=other.label.text))


class InputRequiredIfCheckbox(object):
    """
    Validates that input was provided for this field when a given checkbox is ticked.

    :param checkbox_name:
        The name of the BooleanField to check.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `{field_name}` and `{cbx_name}` if desired.
    :param strip_whitespace:
        If True (the default) also stop the validation chain on input which
        consists of only whitespace.
    """
    def __init__(self, checkbox_name, message=None, strip_whitespace=True):
        self.checkbox_name = checkbox_name
        self.message = message
        if strip_whitespace:
            self.str_check = lambda s: s.strip()
        else:
            self.str_check = lambda s: s

    def __call__(self, form, field):
        try:
            checkbox = form[self.checkbox_name]
        except KeyError:
            raise ValidationError(_(u"Invalid field name '{field_name}'.").format(field_name=self.checkbox_name))

        if not checkbox.data:
            field.errors[:] = []
            raise StopValidation()
        else:
            if not field.raw_data or isinstance(field.raw_data[0], str_types) and not self.str_check(field.raw_data[0]):

                message = self.message
                if message is None:
                    message = _(u"'{field_name}' is required for '{cbx_name}'.")

                field.errors[:] = []
                raise ValidationError(message.format(field_name=field.label.text, cbx_name=checkbox.label.text))
