"""DefaultEncodingConstraint class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultEncodingConstraint


class TestDefaultEncodingConstraint:
    """DefaultEncodingConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_encoding_constraint.DefaultConstraint.__init__")
    def test_init(self, super_mock):
        """Test DefaultEncodingConstraint initialization."""
        result = DefaultEncodingConstraint(self.meta_model_mock, "value")

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._value == "value"

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_encoding_constraint.DefaultConstraint.__init__")
    def test_value(self, _):
        """Test value getter."""
        encoding_constraint = DefaultEncodingConstraint(self.meta_model_mock, "value")
        result = encoding_constraint.value

        assert result == "value"
        assert encoding_constraint._value == "value"

    def test_value_setter(self):
        """Test value setter."""
        encoding_constraint = DefaultEncodingConstraint(self.meta_model_mock, "value")
        encoding_constraint.value = "new_value"

        assert encoding_constraint._value == "new_value"

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_encoding_constraint.DefaultConstraint.__init__")
    def test_value_raise_error(self, _):
        """Test value getter raising exception."""
        encoding_constraint = DefaultEncodingConstraint(self.meta_model_mock, "value")
        with pytest.raises(ValueError) as error:
            encoding_constraint.value = None

        assert str(error.value) == "Value cannot be None."
