"""PropertyInstantiator class unit tests suit."""

from unittest import mock

import pytest

from rdflib import BNode, URIRef

from esmf_aspect_meta_model_python.loader.instantiator.property_instantiator import PropertyInstantiator
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class TestPropertyInstantiator:
    """PropertyInstantiator unit tests class."""

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.PropertyInstantiator."
        "_create_property_direct_reference"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_is_URIRef(self, isinstance_mock, create_property_direct_reference_mock):
        """Test _create_instance for element_node as URIRef."""
        isinstance_mock.return_value = True
        create_property_direct_reference_mock.return_value = "property_instance"
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        result = instantiator_cls._create_instance(element_node_mock)

        assert result == "property_instance"
        isinstance_mock.assert_called_once_with(element_node_mock, URIRef)
        create_property_direct_reference_mock.assert_called_once_with(element_node_mock)

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.PropertyInstantiator."
        "_create_property_blank_node"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_blank_node(self, isinstance_mock, create_property_blank_node_mock):
        """Test _create_instance for element_node as BNode with property value."""
        isinstance_mock.side_effect = (False, True)
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.value.return_value = "value"
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "urn"
        create_property_blank_node_mock.return_value = "property_instance"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._aspect_graph = graph_mock
        instantiator_cls._samm = samm_mock
        result = instantiator_cls._create_instance(element_node_mock)

        assert result == "property_instance"
        isinstance_mock.assert_has_calls(
            [
                mock.call(element_node_mock, URIRef),
                mock.call(element_node_mock, BNode),
            ]
        )
        samm_mock.get_urn.assert_called_once_with(SAMM.property)
        graph_mock.value.assert_called_once_with(subject=element_node_mock, predicate="urn")
        create_property_blank_node_mock.assert_called_once_with(element_node_mock)

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.PropertyInstantiator."
        "_create_property_with_extends"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_node_with_extends(self, isinstance_mock, create_property_with_extends_mock):
        """Test _create_instance for element_node as BNode with extends value."""
        isinstance_mock.side_effect = (False, True)
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.value.side_effect = (None, "value")
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ("urn1", "urn2")
        create_property_with_extends_mock.return_value = "property_instance"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._aspect_graph = graph_mock
        instantiator_cls._samm = samm_mock
        result = instantiator_cls._create_instance(element_node_mock)

        assert result == "property_instance"
        isinstance_mock.assert_has_calls(
            [
                mock.call(element_node_mock, URIRef),
                mock.call(element_node_mock, BNode),
            ]
        )
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.property),
                mock.call(SAMM.extends),
            ]
        )
        graph_mock.value.assert_has_calls(
            [
                mock.call(subject=element_node_mock, predicate="urn1"),
                mock.call(subject=element_node_mock, predicate="urn2"),
            ]
        )
        create_property_with_extends_mock.assert_called_once_with(element_node_mock)

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_raise_exception(self, isinstance_mock):
        """Test _create_instance raises ValueError for invalid element_node type."""
        isinstance_mock.side_effect = (False, False)
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        with pytest.raises(ValueError) as error:
            instantiator_cls._create_instance(element_node_mock)

        assert str(error.value) == "The syntax of the property is not allowed."

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.PropertyInstantiator."
        "_create_property_with_extends"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.isinstance")
    def test_create_instance_element_node_with_extends_raise_exception(
        self,
        isinstance_mock,
        create_property_with_extends_mock,
    ):
        """Test _create_instance for element_node as BNode with extends value."""
        isinstance_mock.side_effect = (False, True)
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.value.side_effect = (None, None)
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ("urn1", "urn2")
        create_property_with_extends_mock.return_value = "property_instance"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._aspect_graph = graph_mock
        instantiator_cls._samm = samm_mock
        with pytest.raises(ValueError) as error:
            instantiator_cls._create_instance(element_node_mock)

        assert str(error.value) == "The syntax of the property is not allowed."

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultProperty")
    def test_create_property_direct_reference(self, default_property_mock):
        """Test _create_property_direct_reference creates DefaultProperty with correct args."""
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        default_property_mock.return_value = "default_property"
        get_base_attributes_mock = mock.MagicMock(name="_get_base_attributes")
        get_base_attributes_mock.return_value = "base_attributes"
        get_child_mock = mock.MagicMock(name="_get_child")
        get_child_mock.return_value = "characteristic"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ("characteristic_urn", "example_value_urn")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "example_value"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._get_base_attributes = get_base_attributes_mock
        instantiator_cls._get_child = get_child_mock
        instantiator_cls._samm = samm_mock
        instantiator_cls._aspect_graph = aspect_graph_mock
        result = instantiator_cls._create_property_direct_reference(element_node_mock)

        assert result == "default_property"
        get_base_attributes_mock.assert_called_once_with(element_node_mock)
        get_child_mock.assert_called_once_with(element_node_mock, "characteristic_urn", required=True)
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.characteristic),
                mock.call(SAMM.example_value),
            ]
        )
        aspect_graph_mock.value.assert_called_once_with(subject=element_node_mock, predicate="example_value_urn")
        default_property_mock.assert_called_once_with(
            meta_model_base_attributes="base_attributes",
            characteristic="characteristic",
            example_value="example_value",
        )

    # @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultBlankProperty")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultProperty")
    def test_create_property_blank_node(self, default_property_mock):
        """Test _create_property_blank_node creates DefaultProperty with correct args."""
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.value.side_effect = [
            "property",
            "optional",
            "not_in_payload",
            "example_value",
        ]
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = [
            "property_urn",
            "optional_urn",
            "not_in_payload_urn",
            "payload_name_urn",
            "characteristic_urn",
            "example_value_urn",
        ]
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        get_child_mock = mock.MagicMock(name="_get_child")
        get_child_mock.side_effect = ["payload_name", "characteristic"]
        get_base_attributes_mock = mock.MagicMock(name="_get_base_attributes")
        get_base_attributes_mock.return_value = "meta_model_base_attributes"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._aspect_graph = graph_mock
        instantiator_cls._samm = samm_mock
        instantiator_cls._get_child = get_child_mock
        instantiator_cls._get_base_attributes = get_base_attributes_mock
        default_property_mock.return_value = "default_property"
        result = instantiator_cls._create_property_blank_node(element_node_mock)

        assert result == "default_property"
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.property),
                mock.call(SAMM.optional),
                mock.call(SAMM.not_in_payload),
                mock.call(SAMM.payload_name),
                mock.call(SAMM.characteristic),
                mock.call(SAMM.example_value),
            ]
        )
        graph_mock.value.assert_has_calls(
            [
                mock.call(subject=element_node_mock, predicate="property_urn"),
                mock.call(subject=element_node_mock, predicate="optional_urn"),
                mock.call(subject=element_node_mock, predicate="not_in_payload_urn"),
                mock.call(subject="property", predicate="example_value_urn"),
            ]
        )
        get_child_mock.assert_has_calls(
            [
                mock.call(element_node_mock, "payload_name_urn"),
                mock.call("property", "characteristic_urn", required=True),
            ]
        )
        get_base_attributes_mock.assert_called_once_with("property")
        default_property_mock.assert_called_once_with(
            meta_model_base_attributes="meta_model_base_attributes",
            characteristic="characteristic",
            example_value="example_value",
            optional=True,
            not_in_payload=True,
            payload_name="payload_name",
        )

    def test_create_property_blank_node_raise_exception(self):
        """Test _create_property_blank_node raises ValueError if property not found."""
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.value.return_value = ""
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "urn"
        element_node_mock = mock.MagicMock(name="element_node")
        element_node_mock.__str__.return_value = "element_node"
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._aspect_graph = graph_mock
        instantiator_cls._samm = samm_mock
        with pytest.raises(ValueError) as error:
            instantiator_cls._create_property_blank_node(element_node_mock)

        assert str(error.value) == "Could not found property for the node element_node"
        samm_mock.get_urn.assert_called_once_with(SAMM.property)
        graph_mock.value.assert_called_once_with(subject=element_node_mock, predicate="urn")

    # @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultPropertyWithExtends")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultProperty")
    def test_create_property_with_extends(self, default_property_with_extends_mock):
        """Test _create_property_with_extends creates DefaultPropertyWithExtends with correct args."""
        element_node_mock = mock.MagicMock(name="element_node")
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.value.return_value = "example_value"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ["payload_name_urn", "extends_urn", "characteristic_urn", "example_value_urn"]
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        default_property_with_extends_mock.return_value = "default_property_with_extends"
        get_child_mock = mock.MagicMock(name="_get_child")
        get_child_mock.side_effect = ["payload_name", "extends", "characteristic"]
        get_base_attributes_mock = mock.MagicMock(name="_get_base_attributes")
        get_base_attributes_mock.return_value = "base_attributes"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._get_base_attributes = get_base_attributes_mock
        instantiator_cls._get_child = get_child_mock
        instantiator_cls._samm = samm_mock
        instantiator_cls._aspect_graph = graph_mock
        result = instantiator_cls._create_property_with_extends(element_node_mock)

        assert result == "default_property_with_extends"
        graph_mock.value.assert_called_once_with(subject=element_node_mock, predicate="example_value_urn")
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.payload_name),
                mock.call(SAMM.extends),
                mock.call(SAMM.characteristic),
            ]
        )
        get_child_mock.assert_has_calls(
            [
                mock.call(element_node_mock, "payload_name_urn"),
                mock.call(element_node_mock, "extends_urn", required=True),
                mock.call(element_node_mock, "characteristic_urn", required=True),
            ]
        )
        default_property_with_extends_mock.assert_called_once_with(
            meta_model_base_attributes="base_attributes",
            characteristic="characteristic",
            example_value="example_value",
            extends="extends",
            payload_name="payload_name",
        )
        get_base_attributes_mock.assert_called_once_with(element_node_mock)
