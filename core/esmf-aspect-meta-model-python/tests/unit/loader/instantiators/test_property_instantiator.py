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
        isinstance_mock.side_effect = (False, False)
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        with pytest.raises(ValueError) as error:
            instantiator_cls._create_instance(element_node_mock)

        assert str(error.value) == "The syntax of the property is not allowed."

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultProperty")
    def test_create_property_direct_reference(self, default_property_mock):
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        default_property_mock.return_value = "default_property"
        get_base_attributes_mock = mock.MagicMock(name="_get_base_attributes")
        get_base_attributes_mock.return_value = "base_attributes"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._get_base_attributes = get_base_attributes_mock
        instantiator_cls._model_element_factory = model_element_factory_mock
        result = instantiator_cls._create_property_direct_reference(element_node_mock)

        assert result == "default_property"
        get_base_attributes_mock.assert_called_once_with(element_node_mock)
        default_property_mock.assert_called_once_with(
            meta_model_base_attributes="base_attributes",
            elements_factory=model_element_factory_mock,
            graph_node=element_node_mock,
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultBlankProperty")
    def test_create_property_blank_node(self, default_blank_property_mock):
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.value.return_value = "property_node"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "urn"
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        element_node_mock = mock.MagicMock(name="element_node")
        get_base_attributes_mock = mock.MagicMock(name="_get_base_attributes")
        get_base_attributes_mock.return_value = "meta_model_base_attributes"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._aspect_graph = graph_mock
        instantiator_cls._samm = samm_mock
        instantiator_cls._get_base_attributes = get_base_attributes_mock
        instantiator_cls._model_element_factory = model_element_factory_mock
        default_blank_property_mock.return_value = "default_blank_property"
        result = instantiator_cls._create_property_blank_node(element_node_mock)

        assert result == "default_blank_property"
        samm_mock.get_urn.assert_called_once_with(SAMM.property)
        graph_mock.value.assert_called_once_with(subject=element_node_mock, predicate="urn")
        get_base_attributes_mock.assert_called_once_with("property_node")
        default_blank_property_mock.assert_called_once_with(
            base_element_node=element_node_mock,
            meta_model_base_attributes="meta_model_base_attributes",
            elements_factory=model_element_factory_mock,
            graph_node="property_node",
        )

    def test_create_property_blank_node_raise_exception(self):
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

        assert str(error.value) == "Could not find property for the node element_node"
        samm_mock.get_urn.assert_called_once_with(SAMM.property)
        graph_mock.value.assert_called_once_with(subject=element_node_mock, predicate="urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.property_instantiator.DefaultPropertyWithExtends")
    def test_create_property_with_extends(self, default_property_with_extends_mock):
        element_node_mock = mock.MagicMock(name="element_node")
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        default_property_with_extends_mock.return_value = "default_property_with_extends"
        get_base_attributes_mock = mock.MagicMock(name="_get_base_attributes")
        get_base_attributes_mock.return_value = "base_attributes"
        instantiator_cls = PropertyInstantiator(model_element_factory_mock)
        instantiator_cls._get_base_attributes = get_base_attributes_mock
        instantiator_cls._model_element_factory = model_element_factory_mock
        result = instantiator_cls._create_property_with_extends(element_node_mock)

        assert result == "default_property_with_extends"
        default_property_with_extends_mock.assert_called_once_with(
            meta_model_base_attributes="base_attributes",
            elements_factory=model_element_factory_mock,
            graph_node=element_node_mock,
        )
        get_base_attributes_mock.assert_called_once_with(element_node_mock)
