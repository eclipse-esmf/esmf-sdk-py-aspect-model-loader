"""EncodingConstraintInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.encoding_constraint_instantiator import (
    EncodingConstraintInstantiator,
)
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestEncodingConstraintInstantiator:
    """EncodingConstraintInstantiator unit tests class."""

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.encoding_constraint_instantiator.DefaultEncodingConstraint"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.instantiator.encoding_constraint_instantiator.RdfHelper.to_python"
    )
    def test_create_instance(self, rdf_helper_mock, default_encoding_constraint_mock):
        base_class_mock = mock.MagicMock(name="EncodingConstraintInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_child.side_effect = ("left", "right")
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "base_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "predicate"
        base_class_mock._samm = samm_mock
        rdf_helper_mock.return_value = "base#value"
        default_encoding_constraint_mock.return_value = "instance"
        result = EncodingConstraintInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        samm_mock.get_urn.assert_called_once_with(SAMM.value)
        aspect_graph_mock.value.assert_called_once_with(subject="element_node", predicate="predicate")
        default_encoding_constraint_mock.assert_called_once_with("meta_model_base_attributes", "value")
