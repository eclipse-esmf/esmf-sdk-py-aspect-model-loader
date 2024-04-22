"""SingleEntityInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG
from esmf_aspect_meta_model_python.loader.instantiator.single_entity_instantiator import SingleEntityInstantiator


class TestSingleEntityInstantiator:
    """SingleEntityInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.single_entity_instantiator.DefaultSingleEntity")
    def test_create_instance(self, default_single_entity_mock):
        base_class_mock = mock.MagicMock(name="SingleEntityInstantiator_class")
        base_class_mock._get_data_type.return_value = "data_type"
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        default_single_entity_mock.return_value = "instance"
        result = SingleEntityInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_data_type.assert_called_once_with("element_node")
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        default_single_entity_mock.assert_called_once_with("meta_model_base_attributes", "data_type")

    def test_create_instance_raise_exception(self):
        base_class_mock = mock.MagicMock(name="SingleEntityInstantiator_class")
        base_class_mock._get_data_type.return_value = None
        with pytest.raises(TypeError) as error:
            SingleEntityInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == DATA_TYPE_ERROR_MSG
