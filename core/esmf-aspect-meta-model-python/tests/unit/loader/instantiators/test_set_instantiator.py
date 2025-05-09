"""SetInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG
from esmf_aspect_meta_model_python.loader.instantiator.set_instantiator import SetInstantiator
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class TestSetInstantiator:
    """SetInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.set_instantiator.DefaultSet")
    def test_create_instance(self, default_set_mock):
        base_class_mock = mock.MagicMock(name="SetInstantiator_class")
        base_class_mock._get_data_type.return_value = "data_type"
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_child.return_value = "element_characteristic"
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "urn"
        base_class_mock._sammc = sammc_mock
        default_set_mock.return_value = "instance"
        result = SetInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_data_type.assert_called_once_with("element_node")
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_child.assert_called_once_with("element_node", "urn")
        sammc_mock.get_urn.assert_called_once_with(SAMMC.element_characteristic)
        default_set_mock.assert_called_once_with("meta_model_base_attributes", "data_type", "element_characteristic")

    def test_create_instance_raise_exception(self):
        base_class_mock = mock.MagicMock(name="SetInstantiator_class")
        base_class_mock._get_data_type.return_value = None
        with pytest.raises(TypeError) as error:
            SetInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == DATA_TYPE_ERROR_MSG
