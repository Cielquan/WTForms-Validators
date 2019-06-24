# [WTForms-Validators](https://github.com/Cielquan/WTForms-Validators)

Additional validators for use in WTForms. This project has no inherent translations, but supports use of 
[flask-babelex](https://github.com/mrjoes/flask-babelex/) to make and use self made translations.

### Built with
* Developed in Python 3.7.3
* Developed with/for WTForms 2.2.1
* Tests made with pytest 4.6.3 - Coverage: 97%

## API

### *class* **wtforms_validators.DecimalDigits**(*min=None, max=None, message=None*):

*Validates that a number has a minimum and/or maximum amount of decimal digits.*
*Only numbers of type `int`, `float` and `decimal` are supported.*

***Parameters:***
* **min** - The minimum required amount of decimal digits. If not provided, minimum value will not be checked.
* **max** - The maximum amount of decimal digits. If not provided, maximum value will not be checked.
* **message** - Error message to raise in case of a validation error. Can be interpolated using `{min}` and `{max}` 
if desired. Useful defaults are provided depending on the existence of min and max. 

### *class* **wtforms_validators.EqualStateTo**(*other_field_name, message=None*):

*Compares the states of two fields.*
*Checks if both field have the same state, like two checkboxes are checked or two inputs are filled.*

***Parameters:***
* **other_field_name** - The name of the other field to compare to.
* **message** - Error message to raise in case of a validation error. Can be interpolated using `{field_name}` 
and `{other_field_name}` if desired.

### *class* **wtforms_validators.InputRequiredIfCheckbox**(*checkbox_name, message=None, strip_whitespace=True*):

*Validates that input was provided for this field when a given checkbox is ticked.*

***Parameters:***
* **checkbox_name** - The name of the BooleanField to check.
* **message** - Error message to raise in case of a validation error. Can be interpolated using `{field_name}` 
and `{cbx_name}` if desired.
* **strip_whitespace** - If True (the default) also stop the validation chain on input which consists of 
only whitespace.

## Rights
This project contains code based on code from [WTForms](https://github.com/wtforms/wtforms) which was modified to 
match the new needs. The rights of the original work lie by the [creators](https://github.com/wtforms) with this 
[license](https://github.com/wtforms/wtforms/blob/master/LICENSE.rst) under Copyright © 2008 by the WTForms team.

## Author
Christian Riedel

## Version and State
Version: 1.0.2

State: 24.06.2019
