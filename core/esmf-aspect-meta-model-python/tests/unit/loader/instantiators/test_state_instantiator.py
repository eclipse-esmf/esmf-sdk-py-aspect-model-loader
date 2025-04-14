"""StructuredValueInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG
from esmf_aspect_meta_model_python.loader.instantiator.state_instantiator import StateInstantiator
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class TestStateInstantiator:
    """StateInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.DefaultState")
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.StateInstantiator."
        "_StateInstantiator__to_state_node_value"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.RdfHelper.get_rdf_list_values")
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.StateInstantiator._get_base_attributes"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.StateInstantiator._get_data_type")
    def test_create_instance(
        self,
        get_data_type_mock,
        get_base_attributes_mock,
        get_rdf_list_values_mock,
        to_state_node_value_mock,
        default_state_mock,
    ):
        get_data_type_mock.return_value = "data_type"
        get_base_attributes_mock.return_value = "meta_model_base_attributes"
        to_state_node_value_mock.side_effect = ("value", "default")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = ("value_collection_node", "defaultValue")
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.side_effect = ("predicate_1", "predicate_2")
        get_rdf_list_values_mock.return_value = ["element_node"]
        model_elements_mock = mock.MagicMock(name="model_elements")
        instantiator = StateInstantiator(model_elements_mock)
        instantiator._aspect_graph = aspect_graph_mock
        instantiator._sammc = sammc_mock
        element_node_mock = mock.MagicMock(name="element_node")
        default_state_mock.return_value = "instance"
        result = instantiator._create_instance(element_node_mock)

        assert result == "instance"
        get_data_type_mock.assert_called_once_with(element_node_mock)
        get_base_attributes_mock.assert_called_once_with(element_node_mock)
        sammc_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMMC.values),
                mock.call(SAMMC.default_value),
            ]
        )
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject=element_node_mock, predicate="predicate_1"),
                mock.call(subject=element_node_mock, predicate="predicate_2"),
            ]
        )
        assert aspect_graph_mock.value.call_count == 2
        get_rdf_list_values_mock.assert_called_once_with("value_collection_node", aspect_graph_mock)
        to_state_node_value_mock.assert_has_calls(
            [
                mock.call("element_node"),
                mock.call("defaultValue"),
            ]
        )
        default_state_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "data_type",
            ["value"],
            "default",
        )

    def test_create_instance_raise_exception(self):
        base_class_mock = mock.MagicMock(name="StateInstantiator_class")
        base_class_mock._get_data_type.return_value = None
        with pytest.raises(TypeError) as error:
            StateInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == DATA_TYPE_ERROR_MSG

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.isinstance")
    def test_to_state_node_value_rdflib_literal(self, isinstance_mock):
        isinstance_mock.return_value = True
        element_node_mock = mock.MagicMock(name="element_node")
        element_node_mock.toPython.return_value = "element_node_value"
        result = StateInstantiator._StateInstantiator__to_state_node_value(
            "base_class",
            element_node_mock,
        )

        assert result == "element_node_value"
        element_node_mock.toPython.assert_called_once()

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.StateInstantiator."
        "_EnumerationInstantiator__is_collection_value"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.isinstance")
    def test_to_state_node_value_rdflib_uriref_state_value(self, isinstance_mock, is_collection_value_mock):
        isinstance_mock.side_effect = (False, True, True, True)
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        property_value_mock = mock.MagicMock(name="property_value")
        property_value_mock.toPython.return_value = "actual_value"
        aspect_graph_mock.predicate_objects.return_value = [("property_urn#property_name", property_value_mock)]
        is_collection_value_mock.return_value = False
        name_urn_mock = mock.MagicMock(name="name_urn")
        name_urn_mock.toPython.return_value = "value_key"
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_urn.return_value = name_urn_mock
        model_elements_mock = mock.MagicMock(name="model_elements")
        instantiator = StateInstantiator(model_elements_mock)
        instantiator._aspect_graph = aspect_graph_mock
        instantiator._samm = samm_mock
        result = instantiator._StateInstantiator__to_state_node_value("value_node#value_node_name")

        assert "property_name" in result
        assert result["property_name"] == "actual_value"
        assert "value_key" in result
        assert result["value_key"] == "value_node_name"
        aspect_graph_mock.predicate_objects.assert_called_once_with("value_node#value_node_name")
        is_collection_value_mock.assert_called_once_with("property_urn#property_name")
        samm_mock.get_urn.assert_called_once_with(SAMM.name)
        name_urn_mock.toPython.assert_called_once()

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.StateInstantiator."
        "_EnumerationInstantiator__instantiate_enum_collection"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.StateInstantiator."
        "_EnumerationInstantiator__is_collection_value"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.isinstance")
    def test_to_state_node_value_rdflib_uriref_collection_value(
        self,
        isinstance_mock,
        is_collection_value_mock,
        instantiate_enum_collection_mock,
    ):
        isinstance_mock.side_effect = (False, True, True)
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.predicate_objects.return_value = [("property_urn#property_name", "property_value")]
        is_collection_value_mock.return_value = True
        instantiate_enum_collection_mock.return_value = "actual_value"
        name_urn_mock = mock.MagicMock(name="name_urn")
        name_urn_mock.toPython.return_value = "value_key"
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_urn.return_value = name_urn_mock
        model_elements_mock = mock.MagicMock(name="model_elements")
        instantiator = StateInstantiator(model_elements_mock)
        instantiator._aspect_graph = aspect_graph_mock
        instantiator._samm = samm_mock
        result = instantiator._StateInstantiator__to_state_node_value("value_node#value_node_name")

        assert "property_name" in result
        assert result["property_name"] == "actual_value"
        assert "value_key" in result
        assert result["value_key"] == "value_node_name"
        aspect_graph_mock.predicate_objects.assert_called_once_with("value_node#value_node_name")
        is_collection_value_mock.assert_called_once_with("property_urn#property_name")
        instantiate_enum_collection_mock.assert_called_once_with("property_value")
        samm_mock.get_urn.assert_called_once_with(SAMM.name)
        name_urn_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.state_instantiator.isinstance")
    def test_to_state_node_value_raise_exception(self, isinstance_mock):
        isinstance_mock.side_effect = (False, False)
        model_elements_mock = mock.MagicMock(name="model_elements")
        instantiator = StateInstantiator(model_elements_mock)
        with pytest.raises(TypeError) as error:
            instantiator._StateInstantiator__to_state_node_value("value_node#value_node_name")

        assert str(error.value) == (
            "Every value of an state must either be a Literal (string, int, etc.) or a URI reference to a ComplexType. "
            "Values of type str are not allowed"
        )
