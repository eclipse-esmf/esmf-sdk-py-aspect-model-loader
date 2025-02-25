"""TraitInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.trait_instantiator import TraitInstantiator
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class TestTraitInstantiator:
    """TraitInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.trait_instantiator.Constraint")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.trait_instantiator.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.trait_instantiator.DefaultTrait")
    def test_create_instance(self, default_trait_mock, isinstance_mock, constraint_mock):
        base_class_mock = mock.MagicMock(name="TraitInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._model_element_factory.create_element.return_value = "element"
        base_class_mock._get_child.return_value = "base_characteristic"
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.side_effect = ("predicate", "urn")
        base_class_mock._sammc = sammc_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.objects.return_value = ["constraint_subject"]
        base_class_mock._aspect_graph = aspect_graph_mock
        default_trait_mock.return_value = "instance"
        isinstance_mock.return_value = True
        result = TraitInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_child.assert_called_once_with("element_node", "urn", required=True)
        base_class_mock._model_element_factory.create_element.assert_called_once_with("constraint_subject")
        aspect_graph_mock.objects.assert_called_once_with(subject="element_node", predicate="predicate")
        sammc_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMMC.constraint),
                mock.call(SAMMC.base_characteristic),
            ]
        )
        default_trait_mock.assert_called_once_with("meta_model_base_attributes", "base_characteristic", ["element"])
        isinstance_mock.assert_called_once_with("element", constraint_mock)

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.trait_instantiator.Constraint")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.trait_instantiator.isinstance")
    def test_create_instance_raise_exception_for_type(self, isinstance_mock, constraint_mock):
        base_class_mock = mock.MagicMock(name="TraitInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._model_element_factory.create_element.return_value = "element"
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.side_effect = ("predicate", "urn")
        base_class_mock._sammc = sammc_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.objects.return_value = ["constraint_subject"]
        base_class_mock._aspect_graph = aspect_graph_mock
        isinstance_mock.return_value = False
        with pytest.raises(ValueError) as error:
            TraitInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == "Trait element_node has element element that is not a Constraint."
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._model_element_factory.create_element.assert_called_once_with("constraint_subject")
        aspect_graph_mock.objects.assert_called_once_with(subject="element_node", predicate="predicate")
        sammc_mock.get_urn.assert_called_once_with(SAMMC.constraint)
        isinstance_mock.assert_called_once_with("element", constraint_mock)

    def test_create_instance_raise_exception(self):
        base_class_mock = mock.MagicMock(name="TraitInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.objects.return_value = []
        with pytest.raises(ValueError) as error:
            TraitInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == "Trait must have at least one constraint."
