"""DatatypeInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.datatype_instantiator import DatatypeInstantiator


class TestDatatypeInstantiator:
    """DatatypeInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.datatype_instantiator.DefaultDataType")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.datatype_instantiator.RdfHelper.to_python")
    def test_create_instance(self, to_python_mock, default_data_type_mock):
        base_class_mock = mock.MagicMock(name="DatatypeInstantiator_class")
        base_class_mock._meta_model_version = "meta_model_version"
        to_python_mock.return_value = "element"
        default_data_type_mock.return_value = "instance"
        result = DatatypeInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        to_python_mock.assert_called_once_with("element_node")
        default_data_type_mock.assert_called_once_with("element", "meta_model_version")

    def test_create_instance_raise_exception(self):
        base_class_mock = mock.MagicMock(name="DatatypeInstantiator_class")
        with pytest.raises(ValueError) as error:
            DatatypeInstantiator._create_instance(base_class_mock, None)

        assert str(error.value) == "Data Type is not specified"
