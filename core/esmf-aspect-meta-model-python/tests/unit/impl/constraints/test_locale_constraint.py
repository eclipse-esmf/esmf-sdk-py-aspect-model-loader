"""DefaultLocaleConstraint class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultLocaleConstraint


class TestDefaultLocaleConstraint:
    """DefaultLocaleConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_locale_constraint.DefaultConstraint.__init__")
    def test_init(self, super_mock):
        """Test DefaultLocaleConstraint initialization."""
        result = DefaultLocaleConstraint(self.meta_model_mock, "locale_code")

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._locale_code == "locale_code"

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_locale_constraint.DefaultConstraint.__init__")
    def test_locale_code(self, _):
        """Test locale_code getter."""
        locale_constraint = DefaultLocaleConstraint(self.meta_model_mock, "locale_code")
        result = locale_constraint.locale_code

        assert result == "locale_code"

    def test_locale_code_setter(self):
        """Test locale_code setter."""
        locale_constraint = DefaultLocaleConstraint(self.meta_model_mock, "locale_code")
        locale_constraint.locale_code = "new_locale_code"

        assert locale_constraint._locale_code == "new_locale_code"

    def test_locale_code_setter_raise_error(self):
        """Test locale_code setter raises ValueError when locale_code is None."""
        locale_constraint = DefaultLocaleConstraint(self.meta_model_mock, "locale_code")
        with pytest.raises(ValueError) as exc_info:
            locale_constraint.locale_code = None

        assert str(exc_info.value) == "Locale code cannot be None."
