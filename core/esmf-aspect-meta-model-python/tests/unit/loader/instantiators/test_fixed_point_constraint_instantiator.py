"""FixedPointConstraintInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.fixed_point_constraint_instantiator import (
    FixedPointConstraintInstantiator,
)
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class TestFixedPointConstraintInstantiator:
    """FixedPointConstraintInstantiator unit tests class."""

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.fixed_point_constraint_instantiator." "RdfHelper.to_python"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.fixed_point_constraint_instantiator."
        "DefaultFixedPointConstraint"
    )
    def test_create_instance(self, default_fixed_point_constraint_mock, to_python_mock):
        base_class_mock = mock.MagicMock(name="FixedPointConstraintInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "value"
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "urn"
        base_class_mock._sammc = sammc_mock
        to_python_mock.side_effect = ("0", "1")
        default_fixed_point_constraint_mock.return_value = "instance"
        result = FixedPointConstraintInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        sammc_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMMC.scale),
                mock.call(SAMMC.integer),
            ]
        )
        aspect_graph_mock.value.assert_has_calls([mock.call(subject="element_node", predicate="urn")])
        assert aspect_graph_mock.value.call_count == 2
        to_python_mock.assert_has_calls([mock.call("value")])
        assert to_python_mock.call_count == 2
        default_fixed_point_constraint_mock.assert_called_once_with("meta_model_base_attributes", 0, 1)
