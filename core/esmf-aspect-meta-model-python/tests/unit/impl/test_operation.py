"""DefaultOperation class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultOperation


class TestDefaultOperation:
    """DefaultOperation unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    input_property_mock = mock.MagicMock(name="input_property")
    output_property_mock = mock.MagicMock(name="output_property")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.default_operation.DefaultOperation._set_parent_element_on_child_elements"
    )
    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.BaseImpl.__init__")
    def test_init(self, super_mock, set_parent_element_on_child_elements_mock):
        """Test __init__ method."""
        result = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._input_properties == [self.input_property_mock]
        assert result._output_property == self.output_property_mock
        set_parent_element_on_child_elements_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.BaseImpl.__init__")
    def test_set_parent_element_on_child_elements(self, _):
        """Test _set_parent_element_on_child_elements method."""
        operation = DefaultOperation(self.meta_model_mock, [None, self.input_property_mock], self.output_property_mock)

        self.input_property_mock.append_parent_element.assert_called_once_with(operation)
        self.output_property_mock.append_parent_element.assert_called_once_with(operation)

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.BaseImpl.__init__")
    def test_input_properties(self, _):
        """Test input_properties property."""
        operation = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)
        result = operation.input_properties

        assert result == [self.input_property_mock]

    def test_input_properties_setter(self):
        """Test input_properties setter."""
        input_property_mock = mock.MagicMock(name="input_property")
        operation = DefaultOperation(self.meta_model_mock, [], self.output_property_mock)
        operation.input_properties = [input_property_mock]
        result = operation.input_properties

        assert result == [input_property_mock]
        assert operation._input_properties == [input_property_mock]
        input_property_mock.append_parent_element.assert_called_once_with(operation)

    def test_input_properties_setter_raise_exception(self):
        """Test exception when input_properties is None."""
        operation = DefaultOperation(self.meta_model_mock, [], self.output_property_mock)
        with pytest.raises(ValueError) as error:
            operation.input_properties = None

        assert str(error.value) == "Operation must have at least one input property."

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.BaseImpl.__init__")
    def test_output_property(self, _):
        """Test output_property property."""
        operation = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)
        result = operation.output_property

        assert result == self.output_property_mock

    def test_output_property_setter(self):
        """Test output_property setter."""
        output_property_mock = mock.MagicMock(name="output_property")
        operation = DefaultOperation(self.meta_model_mock, [self.input_property_mock], None)
        operation.output_property = output_property_mock
        result = operation.output_property

        assert result == output_property_mock
        assert operation._output_property == output_property_mock
        output_property_mock.append_parent_element.assert_called_once_with(operation)

    def test_output_property_setter_none(self):
        """Test output_property setter with None."""
        operation = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)
        operation.output_property = None
        result = operation.output_property

        assert result is None
        assert operation._output_property is None
