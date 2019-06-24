__title__ = 'WTForms-Validators'
__description__ = "Additional validators for WTForms"

__author__ = 'Christian Riedel'
__version__ = '1.0.2'
__version_info__ = (1, 0, 2)

from wtforms_validators import DecimalDigits, EqualStateTo, InputRequiredIfCheckbox

__all__ = ('DecimalDigits', 'EqualStateTo', 'InputRequiredIfCheckbox')
