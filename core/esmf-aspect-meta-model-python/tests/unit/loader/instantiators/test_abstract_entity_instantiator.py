"""AbstractEntityInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.abstract_entity_instantiator import AbstractEntityInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestAbstractEntityInstantiator:
    """AbstractEntityInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_entity_instantiator.DefaultAbstractEntity")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_entity_instantiator.isinstance")
    def test_create_instance(self, isinstance_mock, default_abstract_entity_mock):
        base_class_mock = mock.MagicMock(name="AbstractEntityInstantiator_class")
        base_class_mock._instantiating_now = []
        base_class_mock._get_base_attributes = mock.MagicMock(return_value="meta_model_base_attributes")
        base_class_mock.get_extended_element = mock.MagicMock(return_value="extends_element")
        base_class_mock.get_extending_elements = mock.MagicMock(return_value="extending_subjects")
        base_class_mock._get_list_children = mock.MagicMock(return_value="properties")
        base_class_mock._samm = mock.MagicMock(name="samm_attribute")
        base_class_mock._samm.get_urn = mock.MagicMock(return_value="urn")
        isinstance_mock.return_value = True
        default_abstract_entity_mock.return_value = "result"
        result = AbstractEntityInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "result"
        assert base_class_mock._instantiating_now == []
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock.get_extended_element.assert_called_once_with("element_node")
        base_class_mock.get_extending_elements.assert_called_once_with("element_node")
        base_class_mock._get_list_children.assert_called_once_with("element_node", "urn")
        base_class_mock._samm.get_urn.assert_called_once_with(SAMM.properties)
        default_abstract_entity_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "properties",
            "extends_element",
            "extending_subjects",
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_entity_instantiator.isinstance")
    def test_create_instance_raise_exeption(self, isinstance_mock):
        base_class_mock = mock.MagicMock(name="AbstractEntityInstantiator_class")
        isinstance_mock.return_value = False
        with pytest.raises(TypeError) as error:
            AbstractEntityInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == "An abstract entity needs to be defined as a named node."
