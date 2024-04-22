"""OperationInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.operation_instantiator import OperationInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestOperationInstantiator:
    """OperationInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.operation_instantiator.DefaultOperation")
    def test_create_instance(self, default_operation_mock):
        base_class_mock = mock.MagicMock(name="OperationInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_list_children.return_value = "input"
        base_class_mock._get_child.return_value = "output"
        samm_mock = mock.MagicMock(name="SAMMC")
        samm_mock.get_urn.return_value = "urn"
        base_class_mock._samm = samm_mock
        default_operation_mock.return_value = "instance"
        result = OperationInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_list_children.assert_called_once_with("element_node", "urn")
        base_class_mock._get_child.assert_called_once_with("element_node", "urn")
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.input),
                mock.call(SAMM.output),
            ]
        )
        default_operation_mock.assert_called_once_with("meta_model_base_attributes", "input", "output")
