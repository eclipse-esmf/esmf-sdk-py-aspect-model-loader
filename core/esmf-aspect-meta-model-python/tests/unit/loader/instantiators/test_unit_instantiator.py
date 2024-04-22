"""UnitInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.unit_instantiator import UnitInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestUnitInstantiator:
    """UnitInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.unit_instantiator.DefaultUnit")
    def test_create_instance(self, default_unit_mock):
        base_class_mock = mock.MagicMock(name="UnitInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._UnitInstantiator__get_unit_attribute_as_string.side_effect = (
            "symbol",
            "code",
            "reference_unit",
            "conversion_factor",
        )
        base_class_mock.instantiate_quantity_kind.return_value = "quantity_kind"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ("urn", "urn", "urn", "urn", "predicate")
        base_class_mock._samm = samm_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.objects.return_value = ["quantity_kind_node"]
        base_class_mock._aspect_graph = aspect_graph_mock
        default_unit_mock.return_value = "instance"
        result = UnitInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._UnitInstantiator__get_unit_attribute_as_string.assert_has_calls(
            [
                mock.call("element_node", "urn"),
            ]
        )
        assert base_class_mock._UnitInstantiator__get_unit_attribute_as_string.call_count == 4
        base_class_mock.instantiate_quantity_kind.assert_called_once_with("quantity_kind_node")
        aspect_graph_mock.objects.assert_called_once_with(subject="element_node", predicate="predicate")
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.symbol),
                mock.call(SAMM.common_code),
                mock.call(SAMM.reference_unit),
                mock.call(SAMM.numericConversionFactor),
                mock.call(SAMM.quantity_kind),
            ]
        )
        default_unit_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "symbol",
            "code",
            "reference_unit",
            "conversion_factor",
            {"quantity_kind"},
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.unit_instantiator.DefaultQuantityKind")
    def test_instantiate_quantity_kind(self, default_quantity_kind_mock):
        base_class_mock = mock.MagicMock(name="UnitInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        default_quantity_kind_mock.return_value = "quantity_kind"
        result = UnitInstantiator.instantiate_quantity_kind(base_class_mock, "quantity_kind_subject")

        assert result == "quantity_kind"
        base_class_mock._get_base_attributes.assert_called_once_with("quantity_kind_subject")
        default_quantity_kind_mock.assert_called_once_with("meta_model_base_attributes")

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.unit_instantiator.RdfHelper.to_python")
    def test_get_unit_attribute_as_string(self, to_python_mock):
        base_class_mock = mock.MagicMock(name="UnitInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "attribute_value"
        base_class_mock._aspect_graph = aspect_graph_mock
        to_python_mock.return_value = "attribute_as_string"
        result = UnitInstantiator._UnitInstantiator__get_unit_attribute_as_string(
            base_class_mock,
            "unit_subject",
            "attribute",
        )

        assert result == "attribute_as_string"
        aspect_graph_mock.value.assert_called_once_with("unit_subject", predicate="attribute")
        to_python_mock.assert_called_once_with("attribute_value")
