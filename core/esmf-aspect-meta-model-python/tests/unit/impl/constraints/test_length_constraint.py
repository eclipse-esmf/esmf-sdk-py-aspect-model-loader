"""DefaultLengthConstraint class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultLengthConstraint


class TestDefaultLengthConstraint:
    """DefaultLengthConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_length_constraint.DefaultConstraint.__init__")
    def test_init(self, super_mock):
        """Test DefaultLengthConstraint initialization."""
        result = DefaultLengthConstraint(self.meta_model_mock, 0, 1)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._min_value == 0
        assert result._max_value == 1

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_length_constraint.DefaultConstraint.__init__")
    def test_min_value(self, _):
        """Test min_value getter."""
        length_constraint = DefaultLengthConstraint(self.meta_model_mock, 0, 1)
        result = length_constraint.min_value

        assert result == 0

    def test_min_value_setter(self):
        """Test min_value setter."""
        length_constraint = DefaultLengthConstraint(self.meta_model_mock, 0, 1)
        length_constraint.min_value = 2

        assert length_constraint._min_value == 2

    def test_min_value_setter_raise_error(self):
        """Test min_value setter raises ValueError when min_value is None."""
        length_constraint = DefaultLengthConstraint(self.meta_model_mock, 0, 1)
        with pytest.raises(ValueError) as exc_info:
            length_constraint.min_value = None

        assert str(exc_info.value) == "Min value cannot be None."

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_length_constraint.DefaultConstraint.__init__")
    def test_max_value(self, _):
        """Test max_value getter."""
        length_constraint = DefaultLengthConstraint(self.meta_model_mock, 0, 1)
        result = length_constraint.max_value

        assert result == 1

    def test_max_value_setter(self):
        """Test max_value setter."""
        length_constraint = DefaultLengthConstraint(self.meta_model_mock, 0, 1)
        length_constraint.max_value = 2

        assert length_constraint._max_value == 2

    def test_max_value_setter_raise_error(self):
        """Test max_value setter raises ValueError when max_value is None."""
        length_constraint = DefaultLengthConstraint(self.meta_model_mock, 0, 1)
        with pytest.raises(ValueError) as exc_info:
            length_constraint.max_value = None

        assert str(exc_info.value) == "Max value cannot be None."
