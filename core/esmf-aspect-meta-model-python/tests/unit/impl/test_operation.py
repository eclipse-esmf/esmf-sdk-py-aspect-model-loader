"""DefaultOperation class unit tests suit."""

from unittest import mock

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
        result = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._input_properties == [self.input_property_mock]
        assert result._output_property == self.output_property_mock
        set_parent_element_on_child_elements_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.BaseImpl.__init__")
    def test_set_parent_element_on_child_elements(self, _):
        operation = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)

        self.input_property_mock.append_parent_element.assert_called_once_with(operation)
        self.output_property_mock.append_parent_element.assert_called_once_with(operation)

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.BaseImpl.__init__")
    def test_input_properties(self, _):
        operation = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)
        result = operation.input_properties

        assert result == [self.input_property_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.BaseImpl.__init__")
    def test_output_property(self, _):
        operation = DefaultOperation(self.meta_model_mock, [self.input_property_mock], self.output_property_mock)
        result = operation.output_property

        assert result == self.output_property_mock
