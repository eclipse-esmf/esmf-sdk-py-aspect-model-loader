"""RangeConstraintInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.base.bound_definition import BoundDefinition
from esmf_aspect_meta_model_python.loader.instantiator.range_constraint_instantiator import RangeConstraintInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class TestRangeConstraintInstantiator:
    """RangeConstraintInstantiator unit tests class."""

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.range_constraint_instantiator.DefaultRangeConstraint"
    )
    def test_create_instance(self, default_range_constraint_mock):
        base_class_mock = mock.MagicMock(name="RangeConstraintInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._RangeConstraintInstantiator__get_min_value.return_value = "min_value"
        base_class_mock._RangeConstraintInstantiator__get_max_value.return_value = "max_value"
        base_class_mock._RangeConstraintInstantiator__get_lower_bound_definition.return_value = "lower_bound_definition"
        base_class_mock._RangeConstraintInstantiator__get_upper_bound_definition.return_value = "upper_bound_definition"
        default_range_constraint_mock.return_value = "instance"
        result = RangeConstraintInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._RangeConstraintInstantiator__get_min_value.assert_called_once_with("element_node")
        base_class_mock._RangeConstraintInstantiator__get_max_value.assert_called_once_with("element_node")
        base_class_mock._RangeConstraintInstantiator__get_lower_bound_definition("element_node", "min_value")
        base_class_mock._RangeConstraintInstantiator__get_upper_bound_definition("element_node", "max_value")
        default_range_constraint_mock.assert_called_with(
            "meta_model_base_attributes",
            "min_value",
            "max_value",
            "lower_bound_definition",
            "upper_bound_definition",
        )

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.range_constraint_instantiator."
        "RangeConstraintInstantiator._RangeConstraintInstantiator__get_bound_definition"
    )
    def test_get_upper_bound_definition_range_constraint(self, get_bound_definition_mock):
        base_class_mock = mock.MagicMock(name="RangeConstraintInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "upper_bound_definition_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        base_class_mock._get_data_type.return_value = None
        get_bound_definition_mock.return_value = "instance"
        result = RangeConstraintInstantiator._RangeConstraintInstantiator__get_upper_bound_definition(
            base_class_mock,
            "element_node",
            "max_value",
        )

        assert result == "instance"
        sammc_mock.get_urn.assert_called_once_with(SAMMC.upper_bound_definition)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        get_bound_definition_mock.assert_called_with("upper_bound_definition_value")

    def test_get_upper_bound_definition(self):
        base_class_mock = mock.MagicMock(name="RangeConstraintInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = None
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        base_class_mock._get_data_type.return_value = None
        result = RangeConstraintInstantiator._RangeConstraintInstantiator__get_upper_bound_definition(
            base_class_mock,
            "element_node",
            None,
        )

        assert result == BoundDefinition.OPEN
        sammc_mock.get_urn.assert_called_once_with(SAMMC.upper_bound_definition)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.range_constraint_instantiator."
        "RangeConstraintInstantiator._RangeConstraintInstantiator__get_bound_definition"
    )
    def test_get_lower_bound_definition_range_constraint(self, get_bound_definition_mock):
        base_class_mock = mock.MagicMock(name="RangeConstraintInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "lower_bound_definition_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        base_class_mock._get_data_type.return_value = None
        get_bound_definition_mock.return_value = "instance"
        result = RangeConstraintInstantiator._RangeConstraintInstantiator__get_lower_bound_definition(
            base_class_mock,
            "element_node",
            "max_value",
        )

        assert result == "instance"
        sammc_mock.get_urn.assert_called_once_with(SAMMC.lower_bound_definition)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        get_bound_definition_mock.assert_called_with("lower_bound_definition_value")

    def test_get_lower_bound_definition(self):
        base_class_mock = mock.MagicMock(name="RangeConstraintInstantiator_class")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = None
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        base_class_mock._get_data_type.return_value = None
        result = RangeConstraintInstantiator._RangeConstraintInstantiator__get_lower_bound_definition(
            base_class_mock,
            "element_node",
            None,
        )

        assert result == BoundDefinition.OPEN
        sammc_mock.get_urn.assert_called_once_with(SAMMC.lower_bound_definition)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")

    def test_get_max_value(self):
        base_class_mock = mock.MagicMock(name="RangeConstraintInstantiator_class")
        max_value_mock = mock.MagicMock(name="max_value")
        max_value_mock.toPython.return_value = "max_value"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = max_value_mock
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        base_class_mock._get_data_type.return_value = None
        result = RangeConstraintInstantiator._RangeConstraintInstantiator__get_max_value(
            base_class_mock,
            "element_node",
        )

        assert result == "max_value"
        sammc_mock.get_urn.assert_called_once_with(SAMMC.max_value)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        max_value_mock.toPython.assert_called_once()

    def test_get_min_value(self):
        base_class_mock = mock.MagicMock(name="RangeConstraintInstantiator_class")
        max_value_mock = mock.MagicMock(name="max_value")
        max_value_mock.toPython.return_value = "max_value"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = max_value_mock
        base_class_mock._aspect_graph = aspect_graph_mock
        sammc_mock = mock.MagicMock(name="SAMMC")
        sammc_mock.get_urn.return_value = "predicate"
        base_class_mock._sammc = sammc_mock
        base_class_mock._get_data_type.return_value = None
        result = RangeConstraintInstantiator._RangeConstraintInstantiator__get_min_value(
            base_class_mock,
            "element_node",
        )

        assert result == "max_value"
        sammc_mock.get_urn.assert_called_once_with(SAMMC.min_value)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        max_value_mock.toPython.assert_called_once()

    def test_get_bound_definition(self):
        bound_definition_value_mock = mock.MagicMock(name="bound_definition_value")
        bound_definition_value_mock.toPython.return_value = "bound_definition_value_string#GREATER_THAN"
        result = RangeConstraintInstantiator._RangeConstraintInstantiator__get_bound_definition(
            bound_definition_value_mock,
        )

        assert result == BoundDefinition.GREATER_THAN
        bound_definition_value_mock.toPython.assert_called_once()
