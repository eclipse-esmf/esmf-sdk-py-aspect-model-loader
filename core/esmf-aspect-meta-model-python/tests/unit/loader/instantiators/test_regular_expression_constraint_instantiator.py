"""RegularExpressionConstraintInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.regular_expression_constraint_instantiator import (
    RegularExpressionConstraintInstantiator,
)
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestRegularExpressionConstraintInstantiator:
    """RegularExpressionConstraintInstantiator unit tests class."""

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.regular_expression_constraint_instantiator."
        "DefaultRegularExpressionConstraint"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.regular_expression_constraint_instantiator."
        "RdfHelper.to_python"
    )
    def test_create_instance(self, to_python_mock, default_regular_expression_constraint_mock):
        base_class_mock = mock.MagicMock(name="RegularExpressionConstraintInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        to_python_mock.return_value = "value"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "graph_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        default_regular_expression_constraint_mock.return_value = "instance"
        result = RegularExpressionConstraintInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        samm_mock.get_urn.assert_called_once_with(SAMM.value)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        to_python_mock.assert_called_once_with("graph_value")
        default_regular_expression_constraint_mock.assert_called_once_with("meta_model_base_attributes", "value")
