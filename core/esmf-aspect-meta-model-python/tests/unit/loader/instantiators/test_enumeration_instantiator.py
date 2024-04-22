"""EnumerationInstantiator class unit tests suit."""

from unittest import mock

import pytest
import rdflib

from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG
from esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator import EnumerationInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class TestEnumerationInstantiator:
    """EnumerationInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.DefaultEnumeration")
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.RdfHelper.get_rdf_list_values"
    )
    def test_create_instance(self, get_rdf_list_values_mock, default_enumeration_mock):
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._get_data_type.return_value = "data_type"
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock.get_extended_element.return_value = "extends_element"
        base_class_mock._EnumerationInstantiator__to_enum_node_value.return_value = "value"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "value_collection_node"
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        get_rdf_list_values_mock.return_value = ["value_node"]
        default_enumeration_mock.return_value = "instance"
        result = EnumerationInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_data_type.assert_called_once_with("element_node")
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._EnumerationInstantiator__to_enum_node_value.assert_called_once_with("value_node")
        sammc_mock.get_urn.assert_called_once_with(SAMMC.values)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        get_rdf_list_values_mock.assert_called_once_with("value_collection_node", aspect_graph_mock)
        default_enumeration_mock.assert_called_once_with("meta_model_base_attributes", "data_type", ["value"])

    def test_create_instance_with_exception(self):
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._get_data_type.return_value = None
        with pytest.raises(TypeError) as error:
            EnumerationInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == DATA_TYPE_ERROR_MSG

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_literal(self, isinstance_mock):
        isinstance_mock.return_value = True
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        value_node_mock = mock.MagicMock(name="value_node")
        value_node_mock.toPython.return_value = "node_value"
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(base_class_mock, value_node_mock)

        assert result == "node_value"
        value_node_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_URIRef_collection_value(self, isinstance_mock):
        isinstance_mock.side_effect = (False, True, True)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._EnumerationInstantiator__is_collection_value.return_value = True
        base_class_mock._EnumerationInstantiator__instantiate_enum_collection.return_value = "actual_value"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.predicate_objects.return_value = [
            ("property_urn#property_name", "property_value"),
        ]
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        value_mock = mock.MagicMock(name="value")
        value_mock.toPython.return_value = "value_key"
        samm_mock.get_urn.return_value = value_mock
        base_class_mock._samm = samm_mock
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(
            base_class_mock,
            "value_node#value_node_name",
        )

        assert len(result) == 2
        assert "property_name" in result
        assert result["property_name"] == "actual_value"
        assert "value_key" in result
        assert result["value_key"] == "value_node_name"
        aspect_graph_mock.predicate_objects.assert_called_once_with("value_node#value_node_name")
        base_class_mock._EnumerationInstantiator__is_collection_value.assert_called_once_with(
            "property_urn#property_name",
        )
        base_class_mock._EnumerationInstantiator__instantiate_enum_collection.assert_called_once_with(
            "property_value",
        )
        samm_mock.get_urn.assert_called_once_with(SAMM.name)
        value_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_URIRef_not_collection_value(self, isinstance_mock):
        isinstance_mock.side_effect = (False, True, True)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._EnumerationInstantiator__is_collection_value.return_value = False
        base_class_mock._EnumerationInstantiator__to_enum_node_value.return_value = "actual_value"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.predicate_objects.return_value = [
            ("property_urn#property_name", "property_value"),
        ]
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        value_mock = mock.MagicMock(name="value")
        value_mock.toPython.return_value = "value_key"
        samm_mock.get_urn.return_value = value_mock
        base_class_mock._samm = samm_mock
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(
            base_class_mock,
            "value_node#value_node_name",
        )

        assert len(result) == 2
        assert "property_name" in result
        assert result["property_name"] == "actual_value"
        assert "value_key" in result
        assert result["value_key"] == "value_node_name"
        aspect_graph_mock.predicate_objects.assert_called_once_with("value_node#value_node_name")
        base_class_mock._EnumerationInstantiator__is_collection_value.assert_called_once_with(
            "property_urn#property_name",
        )
        base_class_mock._EnumerationInstantiator__to_enum_node_value.assert_called_once_with(
            "property_value",
        )
        samm_mock.get_urn.assert_called_once_with(SAMM.name)
        value_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_URIRef_raise_exception(self, isinstance_mock):
        isinstance_mock.side_effect = (False, False)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        with pytest.raises(TypeError) as error:
            EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(base_class_mock, "value_node")

        assert str(error.value) == (
            "Every value of an enumeration must either be a Literal (string, int, etc.) or "
            "a URI reference to a ComplexType. Values of type str are not allowed"
        )

    def test_is_collection_value(self):
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = ("characteristic", "characteristic_type")
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.collections_urns.return_value = ["characteristic_type"]
        base_class_mock._sammc = sammc_mock
        result = EnumerationInstantiator._EnumerationInstantiator__is_collection_value(
            base_class_mock,
            "property_subject",
        )

        assert result is True
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="property_subject", predicate="predicate"),
                mock.call(subject="characteristic", predicate=rdflib.RDF.type),
            ]
        )
        samm_mock.get_urn.assert_called_once_with(SAMM.characteristic)
        sammc_mock.collections_urns.assert_called_once()

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.RdfHelper.get_rdf_list_values"
    )
    def test_instantiate_enum_collection(self, get_rdf_list_values_mock):
        get_rdf_list_values_mock.return_value = ["value_node"]
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._aspect_graph = "aspect_graph"
        base_class_mock._EnumerationInstantiator__to_enum_node_value.return_value = "value"
        result = EnumerationInstantiator._EnumerationInstantiator__instantiate_enum_collection(
            base_class_mock,
            "value_list",
        )

        assert result == ["value"]
        get_rdf_list_values_mock.assert_called_once_with("value_list", "aspect_graph")
        base_class_mock._EnumerationInstantiator__to_enum_node_value.assert_called_once_with("value_node")
