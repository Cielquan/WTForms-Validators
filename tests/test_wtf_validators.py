import pytest
from wtforms.validators import StopValidation, ValidationError

from wtforms_validators import DecimalDigits, EqualStateTo, InputRequiredIfCheckbox


class TestDecimalDigits(object):
    """Test 'DecimalDigits` validator"""

    @pytest.mark.parametrize("min_v, max_v", [(1, 2), (2, -1), (2, 2), (-1, 2)])
    def test_decimal_digits(self, min_v, max_v, dummy_form, dummy_field):
        """
        It should pass for the number with correct amount of decimal digits.
        """
        dummy_field.data = 0.12
        validator = DecimalDigits(min_v, max_v)
        validator(dummy_form, dummy_field)

    @pytest.mark.parametrize("min_v, max_v", [(-1, -1), (1, 0)])
    def test_decimal_digits_init_raises(self, min_v, max_v):
        """
        It should raise AssertionError if the validator constructor got wrong values
        """
        with pytest.raises(AssertionError):
            DecimalDigits(min_v, max_v)

    @pytest.mark.parametrize(
        ("validator", "data", "message"),
        (
            (
                DecimalDigits(3, -1),
                "foo",
                """Data type "<class 'str'>" is not a supported.""",
            ),
            (DecimalDigits(3, -1), 0.12, "Number must have at least 3 decimal digits."),
            (DecimalDigits(-1, 1), 0.12, "Number can have at most 1 decimal digit."),
            (DecimalDigits(3, 3), 0.12, "Number must have exactly 3 decimal digits."),
            (
                DecimalDigits(3, 4),
                0.12,
                "Number must have between 3 and 4 decimal digits.",
            ),
        ),
    )
    def test_decimal_digits_messages(
        self, dummy_form, dummy_field, validator, data, message
    ):
        """
        It should raise ValidationError for number with incorrect amount of decimal digits
        """
        dummy_field.data = data
        dummy_field.label = "bar"
        with pytest.raises(ValidationError) as e:
            validator(dummy_form, dummy_field)
        assert str(e.value) == message


class TestEqualStateTo(object):
    """Test 'EqualStateTo` validator"""

    def test_equal_state_to(self, dummy_form, cbx_ticked):
        """
        Equal states should pass.
        """
        dummy_form["foo"] = cbx_ticked
        validator = EqualStateTo("foo")
        validator(dummy_form, cbx_ticked)

    def test_test_equal_state_to_error_messages(
        self, dummy_form, cbx_ticked, cbx_unticked
    ):
        """
        It should raise ValidationError if the states are not equal.
        """
        dummy_form["foo"] = cbx_ticked
        validator = EqualStateTo("foo")
        validator(dummy_form, cbx_unticked)

    @pytest.mark.parametrize(
        ("validator", "message"),
        (
            (EqualStateTo("fo"), "Invalid field name 'fo'."),
            (
                EqualStateTo("foo"),
                "'Checkbox_false' and 'Checkbox_true' must be of equal state.",
            ),
            (EqualStateTo("foo", message="foo"), "foo"),
        ),
    )
    def test_test_equal_state_to_error_messages(
        self, dummy_form, cbx_ticked, cbx_unticked, validator, message
    ):
        """
        It should return error message when the required value is not present when the checkbox is ticked.
        """
        dummy_form["foo"] = cbx_ticked

        with pytest.raises(ValidationError) as e:
            validator(dummy_form, cbx_unticked)
        assert str(e.value) == message


class TestInputRequiredIfCheckbox(object):
    """Test 'InputRequiredIfCheckbox` validator"""

    def test_input_required_if_checkbox(self, dummy_form, cbx_ticked, input_filled):
        """
        It should pass if the required value is present when the checkbox is ticked.
        """
        dummy_form["foo"] = cbx_ticked

        validator = InputRequiredIfCheckbox("foo")
        validator(dummy_form, input_filled)

    def test_input_required_if_checkbox_raises(
        self, dummy_form, cbx_unticked, input_filled
    ):
        """
        It should stop the validation chain if the checkbox is not ticked.
        """
        dummy_form["foo"] = cbx_unticked

        validator = InputRequiredIfCheckbox("foo")
        with pytest.raises(StopValidation):
            validator(dummy_form, input_filled)

    @pytest.mark.parametrize(
        ("validator", "message"),
        (
            (InputRequiredIfCheckbox("fo"), "Invalid field name 'fo'."),
            (
                InputRequiredIfCheckbox("foo"),
                "'Input_empty' is required for 'Checkbox_true'.",
            ),
            (InputRequiredIfCheckbox("foo", message="foo"), "foo"),
        ),
    )
    def test_input_required_if_checkbox_error_message(
        self, dummy_form, cbx_ticked, input_empty, validator, message
    ):
        """
        It should return error message when the required value is not present when the checkbox is ticked.
        """
        dummy_form["foo"] = cbx_ticked

        with pytest.raises(ValidationError) as e:
            validator(dummy_form, input_empty)
        assert str(e.value) == message
