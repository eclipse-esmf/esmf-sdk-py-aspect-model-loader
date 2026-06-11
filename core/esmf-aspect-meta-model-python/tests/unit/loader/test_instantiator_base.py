"""Base Instantiator test suite."""

from unittest import mock
from unittest.mock import MagicMock

import pytest
import rdflib

from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class InstantiatorBaseImpl(InstantiatorBase):
    """InstantiatorBase implementation for testing."""

    def _create_instance(self, element_node):
        """Create instance implementation for testing."""
        return "instance"


class TestInstantiatorBase:
    """InstantiatorBase unit tests class."""

    def test_init(self):
        """Test InstantiatorBase initialization."""
        model_element_factory_mock = MagicMock(name="model_element_factory")
        model_element_factory_mock.get_samm.return_value = "samm"
        model_element_factory_mock.get_sammc.return_value = "sammc"
        model_element_factory_mock.get_unit.return_value = "unit"
        model_element_factory_mock.get_meta_model_version.return_value = "version"
        model_element_factory_mock.get_aspect_graph.return_value = "aspect_graph"
        result = InstantiatorBaseImpl(model_element_factory_mock)

        assert result._model_element_factory == model_element_factory_mock
        assert result._samm == "samm"
        assert result._sammc == "sammc"
        assert result._unit == "unit"
        assert result._meta_model_version == "version"
        assert result._aspect_graph == "aspect_graph"
        assert result._existing_instances == dict()

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.RdfHelper.to_python")
    def test_get_instance(self, to_python_mock):
        """Test get_instance returns an instance from _create_instance."""
        to_python_mock.return_value = "urn"
        instantiator = InstantiatorBaseImpl(MagicMock(name="model_element_factory"))
        instantiator._existing_instances = {"urn": "instance"}
        result = instantiator.get_instance("element_node")

        assert result == "instance"
        to_python_mock.assert_called_once_with("element_node")
        instantiator._existing_instances["urn"] = "instance"

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.RdfHelper.to_python")
    def test_get_instance_no_instance(self, to_python_mock):
        """Test get_instance returns None if no instance exists."""
        to_python_mock.return_value = "urn"
        instantiator = InstantiatorBaseImpl(MagicMock(name="model_element_factory"))
        instantiator._existing_instances = {}
        result = instantiator.get_instance("element_node")

        assert result == "instance"
        to_python_mock.assert_called_once_with("element_node")
        instantiator._existing_instances["urn"] = "instance"

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator_base.MetaModelBaseAttributes.from_meta_model_element"
    )
    def test_get_base_attributes_calls_from_meta_model_element(self, from_meta_model_element_mock):
        """Test _get_base_attributes calls MetaModelBaseAttributes.from_meta_model_element with correct args."""
        model_element_factory_mock = MagicMock(name="model_element_factory")
        model_element_factory_mock.get_samm.return_value = "samm"
        model_element_factory_mock.get_sammc.return_value = "sammc"
        model_element_factory_mock.get_unit.return_value = "unit"
        model_element_factory_mock.get_meta_model_version.return_value = "version"
        model_element_factory_mock.get_aspect_graph.return_value = "aspect_graph"
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        from_meta_model_element_mock.return_value = "base_attributes"
        result = instantiator._get_base_attributes("element_subject")

        assert result == "base_attributes"
        from_meta_model_element_mock.assert_called_once_with(
            "element_subject",
            "aspect_graph",
            "samm",
            "version",
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.RdfHelper.to_python")
    def test_get_child_required_missing_raises(self, to_python_mock):
        """Test _get_child raises ValueError if required child is missing."""
        to_python_mock.return_value = "parent_node_urn"
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = None
        model_element_factory_mock = MagicMock(name="model_element_factory")
        model_element_factory_mock.get_aspect_graph.return_value = aspect_graph_mock
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        with pytest.raises(ValueError) as error:
            instantiator._get_child("parent", "predicate", required=True)

        assert str(error.value) == "Child predicate is required for element parent_node_urn"
        aspect_graph_mock.value.assert_called_once_with(subject="parent", predicate="predicate")

    def test_get_child_optional_missing_returns_none(self):
        """Test _get_child returns None if optional child is missing."""
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = None
        model_element_factory_mock = MagicMock(name="model_element_factory")
        model_element_factory_mock.get_aspect_graph.return_value = aspect_graph_mock
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        result = instantiator._get_child("parent", "predicate", required=False)

        assert result is None
        aspect_graph_mock.value.assert_called_once_with(subject="parent", predicate="predicate")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.RdfHelper.to_python")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.isinstance")
    def test_get_child_literal_returns_converted(self, isinstance_mock, to_python_mock):
        """Test _get_child returns converted value if child is Literal."""
        child_subject_mock = MagicMock(name="child_subject")
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = child_subject_mock
        isinstance_mock.return_value = True
        to_python_mock.return_value = "node_value"
        instantiator = InstantiatorBaseImpl(mock.MagicMock(name="model_element_factory"))
        instantiator._aspect_graph = aspect_graph_mock
        result = instantiator._get_child("parent", "predicate")

        assert result == "node_value"
        aspect_graph_mock.value.assert_called_once_with(subject="parent", predicate="predicate")
        isinstance_mock.assert_called_once_with(child_subject_mock, rdflib.Literal)
        to_python_mock.assert_called_once_with(child_subject_mock)

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.isinstance")
    def test_get_child_sub_element_calls_factory(self, isinstance_mock):
        """Test _get_child calls factory for sub-element child."""
        child_subject_mock = MagicMock(name="child_subject")
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = child_subject_mock
        isinstance_mock.return_value = False
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        model_element_factory_mock.create_element.return_value = "child_node"
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        instantiator._aspect_graph = aspect_graph_mock
        result = instantiator._get_child("parent", "predicate")

        assert result == "child_node"
        aspect_graph_mock.value.assert_called_once_with(subject="parent", predicate="predicate")
        isinstance_mock.assert_called_once_with(child_subject_mock, rdflib.Literal)
        model_element_factory_mock.create_element.assert_called_once_with(
            child_subject_mock,
            "parent",
            attr_name="predicate",
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.RdfHelper.get_rdf_list_values")
    def test_get_list_children(self, get_rdf_list_values_mock):
        """Test _get_list_children returns list of children."""
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "list_node"
        get_rdf_list_values_mock.return_value = ["child_node_1", "child_node_2"]
        model_element_factory_mock = mock.MagicMock(name="model_element_factory")
        model_element_factory_mock.create_element.side_effect = [None, "child_node_instance"]
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        instantiator._aspect_graph = aspect_graph_mock
        result = instantiator._get_list_children("element_subject", "list_predicate")

        assert result == ["child_node_instance"]
        aspect_graph_mock.value.assert_called_once_with(subject="element_subject", predicate="list_predicate")
        get_rdf_list_values_mock.assert_called_once_with("list_node", aspect_graph_mock)
        model_element_factory_mock.create_element.assert_has_calls(
            [
                mock.call("child_node_1", "element_subject", attr_name="list_predicate"),
                mock.call("child_node_2", "element_subject", attr_name="list_predicate"),
            ]
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.isinstance")
    def test_get_data_type_with_element_characteristic_and_data_type(self, isinstance_mock):
        """Test _get_data_type returns DataType instance from element_characteristic with data_type predicate."""
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = [
            "element_characteristic_node",
            "data_type_node",
        ]
        model_element_factory_mock = MagicMock(name="model_element_factory")
        model_element_factory_mock.create_element.return_value = "instance"
        isinstance_mock.return_value = True
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        instantiator._aspect_graph = aspect_graph_mock
        instantiator._samm = MagicMock()
        instantiator._sammc = MagicMock()
        instantiator._samm.get_urn.return_value = "data_type_predicate"
        instantiator._sammc.get_urn.return_value = "element_characteristic_predicate"
        result = instantiator._get_data_type("element_node")

        assert result == "instance"
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="element_node", predicate="element_characteristic_predicate"),
                mock.call(subject="element_characteristic_node", predicate="data_type_predicate"),
            ]
        )
        instantiator._sammc.get_urn.assert_called_once_with(SAMMC.element_characteristic)
        instantiator._samm.get_urn.assert_has_calls(
            [
                mock.call(SAMM.data_type),
                mock.call(SAMM.data_type),
            ]
        )
        model_element_factory_mock.create_element.assert_called_once_with(
            "data_type_node",
            "element_node",
            attr_name="data_type_predicate",
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator_base.isinstance")
    def test_get_data_type_with_element_characteristic_and_no_data_type(self, isinstance_mock):
        """Test _get_data_type tries RDF.type if no data_type found for element_characteristic."""
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = [
            "element_characteristic_node",
            None,
            "data_type_node",
        ]
        model_element_factory_mock = MagicMock(name="model_element_factory")
        model_element_factory_mock.create_element.return_value = "instance"
        isinstance_mock.return_value = False
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        instantiator._aspect_graph = aspect_graph_mock
        instantiator._samm = MagicMock()
        instantiator._sammc = MagicMock()
        instantiator._samm.get_urn.return_value = "data_type_predicate"
        instantiator._sammc.get_urn.return_value = "element_characteristic_predicate"
        result = instantiator._get_data_type("element_node")

        assert result is None
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="element_node", predicate="element_characteristic_predicate"),
                mock.call(subject="element_characteristic_node", predicate="data_type_predicate"),
                mock.call(subject="element_characteristic_node", predicate=rdflib.RDF.type),
            ]
        )
        instantiator._sammc.get_urn.assert_called_once_with(SAMMC.element_characteristic)
        instantiator._samm.get_urn.assert_has_calls(
            [
                mock.call(SAMM.data_type),
                mock.call(SAMM.data_type),
            ]
        )
        model_element_factory_mock.create_element.assert_called_once_with(
            "data_type_node",
            "element_node",
            attr_name="data_type_predicate",
        )

    def test_get_data_type_without_element_characteristic(self):
        """Test _get_data_type gets data_type directly from element_node if no element_characteristic."""
        aspect_graph_mock = MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = [None, None]
        model_element_factory_mock = MagicMock(name="model_element_factory")
        instantiator = InstantiatorBaseImpl(model_element_factory_mock)
        instantiator._aspect_graph = aspect_graph_mock
        instantiator._samm = MagicMock()
        instantiator._sammc = MagicMock()
        instantiator._samm.get_urn.return_value = "data_type_predicate"
        instantiator._sammc.get_urn.return_value = "element_characteristic_predicate"
        result = instantiator._get_data_type("element_node")

        assert result is None
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="element_node", predicate="element_characteristic_predicate"),
                mock.call(subject="element_node", predicate="data_type_predicate"),
            ]
        )
        instantiator._sammc.get_urn.assert_called_once_with(SAMMC.element_characteristic)
        instantiator._samm.get_urn.assert_called_once_with(SAMM.data_type)
