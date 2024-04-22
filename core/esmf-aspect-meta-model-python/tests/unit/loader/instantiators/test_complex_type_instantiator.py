"""ComplexTypeInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.complex_type_instantiator import ComplexTypeInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestComplexTypeInstantiator:
    """ComplexTypeInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.complex_type_instantiator.RdfHelper.to_python")
    def test_get_extended_element_extended_element_node_not_none(self, to_python_mock):
        base_class_mock = mock.MagicMock(name="ComplexTypeInstantiator_class")
        base_class_mock._model_element_factory = mock.MagicMock(return_value="_model_element_factory")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "extended_element_node"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._aspect_graph = aspect_graph_mock
        base_class_mock._samm = samm_mock
        base_class_mock._instantiating_now = []
        to_python_mock.return_value = "extended_element"
        result = ComplexTypeInstantiator.get_extended_element(base_class_mock, "entity_subject")

        assert result == "extended_element"
        aspect_graph_mock.value.assert_called_once_with(subject="entity_subject", predicate="predicate")
        samm_mock.get_urn.assert_called_once_with(SAMM.extends)
        base_class_mock._model_element_factory.create_element.assert_called_once_with("extended_element_node")
        to_python_mock.assert_called_once_with("extended_element_node")

    def test_get_extended_element_extended_element_node_is_none(self):
        base_class_mock = mock.MagicMock(name="ComplexTypeInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = None
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._aspect_graph = aspect_graph_mock
        base_class_mock._samm = samm_mock
        result = ComplexTypeInstantiator.get_extended_element(base_class_mock, "entity_subject")

        assert result is None
        aspect_graph_mock.value.assert_called_once_with(subject="entity_subject", predicate="predicate")
        samm_mock.get_urn.assert_called_once_with(SAMM.extends)

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.complex_type_instantiator.RdfHelper.to_python")
    def test_get_extending_elements(self, to_python_mock):
        base_class_mock = mock.MagicMock(name="ComplexTypeInstantiator_class")
        base_class_mock._model_element_factory = mock.MagicMock(name="model_element_factory")
        base_class_mock._instantiating_now = []
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.subjects.return_value = ["element_subject"]
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        to_python_mock.return_value = "new_element"
        result = ComplexTypeInstantiator.get_extending_elements(base_class_mock, "entity_subject")

        assert result == ["new_element"]
        aspect_graph_mock.subjects.assert_called_once_with(predicate="predicate", object="entity_subject")
        samm_mock.get_urn.assert_called_once_with(SAMM.extends)
        aspect_graph_mock.subjects(predicate="predicate", object="entity_subject")
        base_class_mock._model_element_factory.create_element.assert_called_once_with("element_subject")
        to_python_mock.assert_called_once_with("element_subject")
