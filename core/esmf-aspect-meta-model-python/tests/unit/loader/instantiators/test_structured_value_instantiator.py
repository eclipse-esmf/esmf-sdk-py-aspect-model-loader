"""StructuredValueInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG
from esmf_aspect_meta_model_python.loader.instantiator.structured_value_instantiator import StructuredValueInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class TestStructuredValueInstantiator:
    """StructuredValueInstantiator unit tests class."""

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.structured_value_instantiator.RdfHelper.get_rdf_list_values"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.structured_value_instantiator.RdfHelper.to_python")
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.structured_value_instantiator.DefaultStructuredValue"
    )
    def test_create_instance(self, default_structured_value_mock, to_python_mock, get_rdf_list_values_mock):
        base_class_mock = mock.MagicMock(name="StructuredValueInstantiator_class")
        base_class_mock._get_data_type.return_value = "data_type"
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_child.return_value = "element_characteristic"
        base_class_mock._StructuredValueInstantiator__to_element_node_value.return_value = "element"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = ("deconstruction_rule_value", "element_nodes")
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        to_python_mock.return_value = "deconstruction_rule"
        get_rdf_list_values_mock.return_value = ["element_node"]
        default_structured_value_mock.return_value = "instance"
        result = StructuredValueInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_data_type.assert_called_once_with("element_node")
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        sammc_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMMC.deconstruction_rule),
                mock.call(SAMMC.elements),
            ]
        )
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="element_node", predicate="predicate"),
            ]
        )
        assert aspect_graph_mock.value.call_count == 2
        to_python_mock.assert_called_once_with("deconstruction_rule_value")
        get_rdf_list_values_mock.assert_called_once_with("element_nodes", aspect_graph_mock)
        base_class_mock._StructuredValueInstantiator__to_element_node_value.assert_called_once_with("element_node")
        default_structured_value_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "data_type",
            "deconstruction_rule",
            ["element"],
        )

    def test_create_instance_raise_exception(self):
        base_class_mock = mock.MagicMock(name="StructuredValueInstantiator_class")
        base_class_mock._get_data_type.return_value = None
        with pytest.raises(TypeError) as error:
            StructuredValueInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == DATA_TYPE_ERROR_MSG

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.structured_value_instantiator.isinstance")
    def test_to_element_node_value_literal(self, isinstance_mock):
        isinstance_mock.return_value = True
        element_node_mock = mock.MagicMock(name="element_node")
        element_node_mock.toPython.return_value = "element_node_value"
        result = StructuredValueInstantiator._StructuredValueInstantiator__to_element_node_value(
            "base_class",
            element_node_mock,
        )

        assert result == "element_node_value"
        element_node_mock.toPython.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.structured_value_instantiator.isinstance")
    def test_to_element_node_value(self, isinstance_mock):
        isinstance_mock.return_value = False
        base_class_mock = mock.MagicMock(name="StructuredValueInstantiator_class")
        base_class_mock._model_element_factory.create_element.return_value = "element_node_value"
        result = StructuredValueInstantiator._StructuredValueInstantiator__to_element_node_value(
            base_class_mock,
            "element_node",
        )

        assert result == "element_node_value"
        base_class_mock._model_element_factory.create_element.assert_called_once_with("element_node")
