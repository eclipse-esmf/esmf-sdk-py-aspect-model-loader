"""EnumerationInstantiator class unit tests suit."""

from unittest import mock

import pytest
import rdflib

from esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator import EnumerationInstantiator
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class TestEnumerationInstantiator:
    """EnumerationInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.DefaultEnumeration")
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.RdfHelper.get_rdf_list_values"
    )
    def test_create_instance(self, get_rdf_list_values_mock, default_enumeration_mock):
        """Test _create_instance method."""
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

    def test_get_name(self):
        """Test _get_node_name returns name from node URI."""
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        result = EnumerationInstantiator._get_node_name(base_class_mock, "value_node#value_node_name", {})

        assert result == "value_node_name"

    def test_get_node_name_with_preferred_name(self):
        """Test _get_node_name with preferredName property."""
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        result = EnumerationInstantiator._get_node_name(
            base_class_mock, "value_node", {"preferredName": "My Preferred Name"}
        )

        assert result == "MyPreferredName"

    def test_get_node_name_with_value(self):
        """Test _get_node_name with value property."""
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        result = EnumerationInstantiator._get_node_name(base_class_mock, "value_node", {"value": "SomeValue"})

        assert result == "SomeValue"

    def test_get_node_name_with_fallback(self):
        """Test _get_node_name fallback to node URI."""
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        result = EnumerationInstantiator._get_node_name(base_class_mock, "value_node", {})

        assert result == "value_node"

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_get_complex_data_type_value(self, isinstance_mock):
        """Test _get_complex_data_type_value with collection value."""
        isinstance_mock.side_effect = (False, True)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._EnumerationInstantiator__is_collection_value.return_value = True
        base_class_mock._EnumerationInstantiator__instantiate_enum_collection.return_value = "property_actual_value"
        base_class_mock._get_node_name.return_value = "value_node_name"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.predicate_objects.return_value = [
            ("property_urn#entity", "entity_value"),
            ("property_urn#property", "property_value"),
        ]
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        value_mock = mock.MagicMock(name="value")
        value_mock.toPython.return_value = "value_key"
        samm_mock.get_urn.return_value = value_mock
        base_class_mock._samm = samm_mock
        result = EnumerationInstantiator._get_complex_data_type_value(
            base_class_mock,
            "value_node#value_node_name",
        )

        assert len(result) == 2
        assert "property" in result
        assert result["property"] == "property_actual_value"
        assert "value_key" in result
        assert result["value_key"] == "value_node_name"
        aspect_graph_mock.predicate_objects.assert_called_once_with("value_node#value_node_name")
        base_class_mock._EnumerationInstantiator__is_collection_value.assert_called_once_with("property_urn#property")
        base_class_mock._EnumerationInstantiator__instantiate_enum_collection.assert_called_once_with("property_value")
        samm_mock.get_urn.assert_called_once_with(SAMM.name)
        value_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_get_complex_data_type_value_see_property(self, isinstance_mock):
        """Test _get_complex_data_type_value with see property."""
        isinstance_mock.side_effect = (True, True)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._EnumerationInstantiator__is_collection_value.side_effect = (False, False)
        base_class_mock._EnumerationInstantiator__to_enum_node_value.side_effect = ("actual_value_1", "actual_value_2")
        base_class_mock._get_node_name.return_value = "value_node_name"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.predicate_objects.return_value = [
            ("property_urn#see", "property_value_1"),
            ("property_urn#see", "property_value_2"),
        ]
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        value_mock = mock.MagicMock(name="value")
        value_mock.toPython.return_value = "value_key"
        samm_mock.get_urn.return_value = value_mock
        base_class_mock._samm = samm_mock
        result = EnumerationInstantiator._get_complex_data_type_value(
            base_class_mock,
            "value_node#value_node_name",
        )

        assert len(result) == 2
        assert "see" in result
        assert sorted(result["see"]) == ["actual_value_1", "actual_value_2"]
        assert "value_key" in result
        assert result["value_key"] == "value_node_name"
        aspect_graph_mock.predicate_objects.assert_called_once_with("value_node#value_node_name")
        base_class_mock._EnumerationInstantiator__is_collection_value.assert_has_calls(
            [
                mock.call("property_urn#see"),
                mock.call("property_urn#see"),
            ]
        )
        base_class_mock._EnumerationInstantiator__to_enum_node_value.assert_has_calls(
            [
                mock.call("property_value_1"),
                mock.call("property_value_2"),
            ]
        )
        samm_mock.get_urn.assert_called_once_with(SAMM.name)
        value_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_literal(self, isinstance_mock):
        """Test __to_enum_node_value with Literal node."""
        isinstance_mock.return_value = True
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        value_node_mock = mock.MagicMock(name="value_node")
        value_node_mock.toPython.return_value = "node_value"
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(base_class_mock, value_node_mock)

        assert result == "node_value"
        value_node_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_ref(self, isinstance_mock):
        """Test __to_enum_node_value with Ref node."""
        isinstance_mock.side_effect = (False, True)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        value_node_mock = mock.MagicMock(name="value_node")
        value_node_mock.find.return_value = -1
        value_node_mock.toPython.return_value = "node_value"
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(base_class_mock, value_node_mock)

        assert result == "node_value"
        value_node_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_URIRef_collection_value(self, isinstance_mock):
        """Test __to_enum_node_value with URIRef collection value."""
        isinstance_mock.side_effect = (False, False, True)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._get_complex_data_type_value.return_value = "dict_value"
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(
            base_class_mock,
            "value_node#value_node_name",
        )

        assert result == "dict_value"
        base_class_mock._get_complex_data_type_value.assert_called_once_with("value_node#value_node_name")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_BNode(self, isinstance_mock):
        """Test __to_enum_node_value with BNode value."""
        isinstance_mock.side_effect = (False, False, False, True)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        base_class_mock._get_complex_data_type_value.return_value = "dict_value"
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(
            base_class_mock,
            "value_node#value_node_name",
        )

        assert result == "dict_value"
        base_class_mock._get_complex_data_type_value.assert_called_once_with("value_node#value_node_name")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_URIRef_raise_exception(self, isinstance_mock):
        """Test __to_enum_node_value raises TypeError for URIRef value."""
        isinstance_mock.side_effect = (False, False, False, False)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        with pytest.raises(TypeError) as error:
            EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(
                base_class_mock,
                rdflib.namespace.RDF.nil,
            )

        assert str(error.value) == (
            "Every value of an enumeration must either be a Literal (string, int, etc.) or "
            "a URI reference to a ComplexType. Values of type URIRef are not allowed"
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator.isinstance")
    def test_to_enum_node_value_node_is_Variable(self, isinstance_mock):
        """Test __to_enum_node_value with Variable node returns empty string."""
        isinstance_mock.side_effect = (False, False, False, False)
        base_class_mock = mock.MagicMock(name="EnumerationInstantiator_class")
        result = EnumerationInstantiator._EnumerationInstantiator__to_enum_node_value(
            base_class_mock,
            rdflib.Variable("value_node"),
        )

        assert result == ""

    def test_is_collection_value(self):
        """Test __is_collection_value returns True for collection type."""
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
        """Test __instantiate_enum_collection returns list of values."""
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
