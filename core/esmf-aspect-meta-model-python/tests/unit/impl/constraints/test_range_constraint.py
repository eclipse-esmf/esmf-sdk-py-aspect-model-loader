"""DefaultRangeConstraint class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultRangeConstraint


class TestDefaultRangeConstraint:
    """DefaultRangeConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    lower_bound_definition_mock = mock.MagicMock(name="lower_bound_definition")
    upper_bound_definition_mock = mock.MagicMock(name="upper_bound_definition")

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_range_constraint.DefaultConstraint.__init__")
    def test_init(self, super_mock):
        """Test DefaultRangeConstraint initialization."""
        result = DefaultRangeConstraint(
            self.meta_model_mock, 0, 1, self.lower_bound_definition_mock, self.upper_bound_definition_mock
        )

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._min_value == 0
        assert result._max_value == 1
        assert result._lower_bound_definition == self.lower_bound_definition_mock
        assert result._upper_bound_definition == self.upper_bound_definition_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_range_constraint.DefaultConstraint.__init__")
    def test_min_value(self, _):
        """Test min_value getter."""
        range_constraint = DefaultRangeConstraint(
            self.meta_model_mock, 0, 1, self.lower_bound_definition_mock, self.upper_bound_definition_mock
        )
        result = range_constraint.min_value

        assert result == 0

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_range_constraint.DefaultConstraint.__init__")
    def test_max_value(self, _):
        """Test max_value getter."""
        range_constraint = DefaultRangeConstraint(
            self.meta_model_mock, 0, 1, self.lower_bound_definition_mock, self.upper_bound_definition_mock
        )
        result = range_constraint.max_value

        assert result == 1

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_range_constraint.DefaultConstraint.__init__")
    def test_lower_bound_definition(self, _):
        """Test lower_bound_definition getter."""
        range_constraint = DefaultRangeConstraint(
            self.meta_model_mock, 0, 1, self.lower_bound_definition_mock, self.upper_bound_definition_mock
        )
        result = range_constraint.lower_bound_definition

        assert result == self.lower_bound_definition_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_range_constraint.DefaultConstraint.__init__")
    def test_upper_bound_definition(self, _):
        """Test upper_bound_definition getter."""
        range_constraint = DefaultRangeConstraint(
            self.meta_model_mock, 0, 1, self.lower_bound_definition_mock, self.upper_bound_definition_mock
        )
        result = range_constraint.upper_bound_definition

        assert result == self.upper_bound_definition_mock
