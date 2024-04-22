"""AbstractPropertyInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.abstract_property_instantiator import (
    AbstractPropertyInstantiator,
)
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestAbstractPropertyInstantiator:
    """AbstractPropertyInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_property_instantiator.isinstance")
    def test_create_instance_URIRef(self, isinstance_mock):
        base_class_mock = mock.MagicMock(name="AbstractPropertyInstantiator_class")
        base_class_mock._create_property_direct_reference = mock.MagicMock(return_value="property")
        isinstance_mock.return_value = True
        result = AbstractPropertyInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "property"
        base_class_mock._create_property_direct_reference.assert_called_once_with("element_node")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_property_instantiator.isinstance")
    def test_create_instance_BNode(self, isinstance_mock):
        base_class_mock = mock.MagicMock(name="AbstractPropertyInstantiator_class")
        base_class_mock._create_property_blank_node = mock.MagicMock(return_value="property")
        isinstance_mock.side_effect = (False, True)
        result = AbstractPropertyInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "property"
        base_class_mock._create_property_blank_node.assert_called_once_with("element_node")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_entity_instantiator.isinstance")
    def test_create_instance_raise_exeption(self, isinstance_mock):
        base_class_mock = mock.MagicMock(name="AbstractPropertyInstantiator_class")
        isinstance_mock.side_effect = (False, False)
        with pytest.raises(ValueError) as error:
            AbstractPropertyInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == "Invalid syntax for Abstract Property"

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_property_instantiator.DefaultProperty")
    def test_create_property_direct_reference(self, default_property_mock):
        base_class_mock = mock.MagicMock(name="AbstractPropertyInstantiator_class")
        base_class_mock._get_base_attributes = mock.MagicMock(return_value="meta_model_base_attributes")
        aspect_graph_mock = mock.MagicMock(name="AspectGraph")
        aspect_graph_mock.value.return_value = "example_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        default_property_mock.return_value = "default_property"
        result = AbstractPropertyInstantiator._create_property_direct_reference(
            base_class_mock,
            "element_node",
        )

        assert result == "default_property"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        samm_mock.get_urn.assert_called_once_with(SAMM.example_value)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        default_property_mock.assert_called_once_with(
            "meta_model_base_attributes",
            characteristic=None,
            example_value="example_value",
            abstract=True,
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.abstract_property_instantiator.DefaultProperty")
    def test_create_property_blank_node(self, default_property_mock):
        base_class_mock = mock.MagicMock(name="AbstractPropertyInstantiator_class")
        base_class_mock._get_child.return_value = "payload_name"
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        aspect_graph_mock = mock.MagicMock(name="AspectGraph")
        aspect_graph_mock.value.side_effect = ("optional", "not_in_payload", "property_node", "example_value")
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        default_property_mock.return_value = "default_property"
        result = AbstractPropertyInstantiator._create_property_blank_node(
            base_class_mock,
            "element_node",
        )

        assert result == "default_property"
        aspect_graph_mock.value.has_call(
            [
                mock.call(subject="element_node", predicate="predicate"),
            ]
        )
        assert aspect_graph_mock.value.call_count == 4
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.optional),
                mock.call(SAMM.not_in_payload),
                mock.call(SAMM.payload_name),
                mock.call(SAMM.property),
                mock.call(SAMM.example_value),
            ]
        )
        base_class_mock._get_child.assert_called_once_with("element_node", "predicate")
        base_class_mock._get_base_attributes.assert_called_once_with("property_node")
        default_property_mock.assert_called_once_with(
            "meta_model_base_attributes",
            characteristic=None,
            example_value="example_value",
            abstract=True,
            optional=True,
            not_in_payload=True,
            payload_name="payload_name",
        )
