import pytest


@pytest.fixture
def dummy_form():
    return DummyForm()


@pytest.fixture
def dummy_field():
    return DummyField


@pytest.fixture
def cbx_ticked(dummy_field):
    cbx = dummy_field()
    cbx.raw_data = ["y"]
    cbx.data = True
    cbx.label = "Checkbox_true"
    return cbx


@pytest.fixture
def cbx_unticked(dummy_field):
    cbx = dummy_field()
    cbx.raw_data = []
    cbx.data = False
    cbx.label = "Checkbox_false"
    return cbx


@pytest.fixture
def input_filled(dummy_field):
    f = dummy_field()
    f.raw_data = ["foobar"]
    f.data = "foobar"
    f.label = "Input_filled"
    return f


@pytest.fixture
def input_empty(dummy_field):
    f = dummy_field()
    f.raw_data = []
    f.data = False
    f.label = "Input_empty"
    return f


class DummyTranslations(object):
    def gettext(self, string):
        return string

    def ngettext(self, singular, plural, n):
        if n == 1:
            return singular

        return plural


class DummyField(object):
    _translations = DummyTranslations()

    def __init__(
        self,
        data=None,
        name=None,
        errors=(),
        raw_data=None,
        label=None,
        id=None,
        field_type="StringField",
    ):
        self.data = data
        self.name = name
        self.errors = list(errors)
        self.raw_data = raw_data
        self.label = label
        self.id = id if id else ""
        self.type = field_type

    def __call__(self, **other):
        return self.data

    def __str__(self):
        return self.data

    def __unicode__(self):
        return self.data

    def __iter__(self):
        return iter(self.data)

    def _value(self):
        return self.data

    def iter_choices(self):
        return iter(self.data)

    def gettext(self, string):
        return self._translations.gettext(string)

    def ngettext(self, singular, plural, n):
        return self._translations.ngettext(singular, plural, n)


class DummyForm(dict):
    pass
