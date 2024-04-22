"""EntityInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.entity_instantiator import EntityInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestEntityInstantiator:
    """EntityInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.entity_instantiator.DefaultEntity")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.entity_instantiator.isinstance")
    def test_create_instance(self, isinstance_mock, default_entity_mock):
        isinstance_mock.return_value = True
        base_class_mock = mock.MagicMock(name="EntityInstantiator_class")
        base_class_mock._instantiating_now = []
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock.get_extended_element.return_value = "extends_element"
        base_class_mock._get_list_children.return_value = "properties"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "urn"
        base_class_mock._samm = samm_mock
        default_entity_mock.return_value = "instance"
        result = EntityInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock.get_extended_element.assert_called_once_with("element_node")
        base_class_mock._get_list_children.assert_called_once_with("element_node", "urn")
        samm_mock.get_urn.assert_called_once_with(SAMM.properties)
        default_entity_mock.assert_called_once_with("meta_model_base_attributes", "properties", "extends_element")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.entity_instantiator.isinstance")
    def test_create_instance_with_exception(self, isinstance_mock):
        isinstance_mock.return_value = False
        base_class_mock = mock.MagicMock(name="EntityInstantiator_class")
        with pytest.raises(TypeError) as error:
            EntityInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == "An Entity needs to be defined as a named node"
