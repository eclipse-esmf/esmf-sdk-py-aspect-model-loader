"""LanguageConstraintInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.language_constraint_instantiator import (
    LanguageConstraintInstantiator,
)
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class TestLanguageConstraintInstantiator:
    """LanguageConstraintInstantiator unit tests class."""

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.language_constraint_instantiator.RdfHelper.to_python"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.language_constraint_instantiator."
        "DefaultLanguageConstraint"
    )
    def test_create_instance(self, default_language_constraint_mock, to_python_mock):
        base_class_mock = mock.MagicMock(name="LanguageConstraintInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "value"
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        to_python_mock.return_value = "language_code"
        default_language_constraint_mock.return_value = "instance"
        result = LanguageConstraintInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        sammc_mock.get_urn.assert_called_once_with(SAMMC.language_code)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        to_python_mock.assert_called_once_with("value")
        default_language_constraint_mock.assert_called_once_with("meta_model_base_attributes", "language_code")
