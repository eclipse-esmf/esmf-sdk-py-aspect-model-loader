"""DefaultLocaleConstraint class unit tests suit."""

from unittest import mock

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
