"""DefaultFixedPointConstraint class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultFixedPointConstraint


class TestDefaultFixedPointConstraint:
    """DefaultFixedPointConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_fixed_point_constraint.DefaultConstraint.__init__"
    )
    def test_init(self, super_mock):
        """Test DefaultFixedPointConstraint initialization."""
        result = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._scale == 0
        assert result._integer == 1

    def test_scale_setter(self):
        """Test scale setter."""
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        fixed_point_constraint.scale = 2

        assert fixed_point_constraint._scale == 2

    def test_scale_setter_raise_error(self):
        """Test scale setter raises ValueError when scale is None."""
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        with pytest.raises(ValueError) as exc_info:
            fixed_point_constraint.scale = None

        assert str(exc_info.value) == "Scale cannot be None."

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_fixed_point_constraint.DefaultConstraint.__init__"
    )
    def test_value(self, _):
        """Test scale getter."""
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        result = fixed_point_constraint.scale

        assert result == 0

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_fixed_point_constraint.DefaultConstraint.__init__"
    )
    def test_integer(self, _):
        """Test integer getter."""
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        result = fixed_point_constraint.integer

        assert result == 1

    def test_integer_setter(self):
        """Test integer setter."""
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        fixed_point_constraint.integer = 2

        assert fixed_point_constraint._integer == 2

    def test_integer_setter_raise_error(self):
        """Test integer setter raises ValueError when integer is None."""
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        with pytest.raises(ValueError) as exc_info:
            fixed_point_constraint.integer = None

        assert str(exc_info.value) == "Integer cannot be None."
