"""DefaultRegularExpressionConstraint class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultRegularExpressionConstraint


class TestDefaultRegularExpressionConstraint:
    """DefaultRangeConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    lower_bound_definition_mock = mock.MagicMock(name="lower_bound_definition")
    upper_bound_definition_mock = mock.MagicMock(name="upper_bound_definition")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_regular_expression_constraint."
        "DefaultConstraint.__init__"
    )
    def test_init(self, super_mock):
        """Test DefaultRegularExpressionConstraint initialization."""
        result = DefaultRegularExpressionConstraint(self.meta_model_mock, "value")

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._value == "value"

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_regular_expression_constraint."
        "DefaultConstraint.__init__"
    )
    def test_value(self, _):
        """Test value getter."""
        regular_expression_constraint = DefaultRegularExpressionConstraint(self.meta_model_mock, "value")
        result = regular_expression_constraint.value

        assert result == "value"
