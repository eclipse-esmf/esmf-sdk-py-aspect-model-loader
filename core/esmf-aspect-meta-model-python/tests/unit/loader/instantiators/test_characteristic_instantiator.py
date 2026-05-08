"""CharacteristicInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.characteristic_instantiator import CharacteristicInstantiator


class TestCharacteristicInstantiator:
    """CharacteristicInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.characteristic_instantiator.DefaultCharacteristic")
    def test_create_instance(self, default_characteristic_mock):
        base_class_mock = mock.MagicMock(name="CharacteristicInstantiator_class")
        base_class_mock._get_data_type = mock.MagicMock(return_value="data_type")
        base_class_mock._get_base_attributes = mock.MagicMock(return_value="meta_model_base_attributes")
        default_characteristic_mock.return_value = "characteristic"
        result = CharacteristicInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "characteristic"
        base_class_mock._get_data_type.assert_called_once_with("element_node")
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        default_characteristic_mock.assert_called_once_with("meta_model_base_attributes", "data_type")
