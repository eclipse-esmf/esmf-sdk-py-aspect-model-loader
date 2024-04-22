"""PropertyInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.property_instantiator import PropertyInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestPropertyInstantiator:
    """PropertyInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_is_URIRef(self, isinstance_mock):
        isinstance_mock.return_value = True
        base_class_mock = mock.MagicMock(name="PropertyInstantiator_class")
        base_class_mock._create_property_direct_reference.return_value = "instance"
        result = PropertyInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._create_property_direct_reference.assert_called_once_with("element_node")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_blank_node(self, isinstance_mock):
        isinstance_mock.side_effect = (False, True)
        base_class_mock = mock.MagicMock(name="PropertyInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "value"
        base_class_mock._aspect_graph = aspect_graph_mock
        base_class_mock._create_property_blank_node.return_value = "instance"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        result = PropertyInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        samm_mock.get_urn.assert_called_once_with(SAMM.property)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        base_class_mock._create_property_blank_node.assert_called_once_with("element_node")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_node_with_extends(self, isinstance_mock):
        isinstance_mock.side_effect = (False, True)
        base_class_mock = mock.MagicMock(name="PropertyInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = (None, "value")
        base_class_mock._aspect_graph = aspect_graph_mock
        base_class_mock._create_property_with_extends.return_value = "instance"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        result = PropertyInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.property),
                mock.call(SAMM.extends),
            ]
        )
        aspect_graph_mock.value.assert_has_calls([mock.call(subject="element_node", predicate="predicate")])
        assert aspect_graph_mock.value.call_count == 2
        base_class_mock._create_property_with_extends.assert_called_once_with("element_node")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_raise_exception(self, isinstance_mock):
        isinstance_mock.side_effect = (False, False)
        base_class_mock = mock.MagicMock(name="PropertyInstantiator_class")
        with pytest.raises(ValueError) as error:
            PropertyInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == "The syntax of the property is not allowed."

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultProperty")
    def test_create_property_direct_reference(self, default_property_mock):
        base_class_mock = mock.MagicMock(name="PropertyInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_child.return_value = "characteristic"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ("urn", "predicate")
        base_class_mock._samm = samm_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "example_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        default_property_mock.return_value = "instance"
        result = PropertyInstantiator._create_property_direct_reference(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_child.assert_called_once_with("element_node", "urn", required=True)
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.characteristic),
                mock.call(SAMM.example_value),
            ]
        )
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        default_property_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "characteristic",
            "example_value",
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultProperty")
    def test_create_property_blank_node(self, default_property_mock):
        base_class_mock = mock.MagicMock(name="PropertyInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_child.return_value = "characteristic"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = (
            "predicate",
            "predicate",
            "urn",
            "predicate",
            "urn",
            "predicate",
        )
        base_class_mock._samm = samm_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = ("optional", "not_in_payload", "property_node", "example_value")
        base_class_mock._aspect_graph = aspect_graph_mock
        default_property_mock.return_value = "instance"
        result = PropertyInstantiator._create_property_blank_node(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("property_node")
        base_class_mock._get_child.assert_has_calls(
            [
                mock.call("element_node", "urn"),
                mock.call("property_node", "urn", required=True),
            ]
        )
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.characteristic),
                mock.call(SAMM.example_value),
            ]
        )
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="element_node", predicate="predicate"),
                mock.call(subject="property_node", predicate="predicate"),
            ]
        )
        default_property_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "characteristic",
            "example_value",
            optional=True,
            not_in_payload=True,
            payload_name="characteristic",
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultProperty")
    def test_create_property_with_extends(self, default_property_mock):
        base_class_mock = mock.MagicMock(name="PropertyInstantiator_class")
        base_class_mock._get_child.side_effect = ("payload_name", "extends", "characteristic")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = (
            "urn",
            "urn",
            "urn",
            "predicate",
        )
        base_class_mock._samm = samm_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "example_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        default_property_mock.return_value = "instance"
        result = PropertyInstantiator._create_property_with_extends(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_child.assert_has_calls(
            [
                mock.call("element_node", "urn"),
                mock.call("element_node", "urn", required=True),
            ]
        )
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.payload_name),
                mock.call(SAMM.extends),
                mock.call(SAMM.characteristic),
                mock.call(SAMM.example_value),
            ]
        )
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        default_property_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "characteristic",
            "example_value",
            "extends",
            payload_name="payload_name",
        )
