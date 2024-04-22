"""CodeInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.code_instantiator import CodeInstantiator
from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG


class TestCodeInstantiator:
    """CodeInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.code_instantiator.DefaultCode")
    def test_create_instance(self, default_code_mock):
        base_class_mock = mock.MagicMock(name="CodeInstantiator_class")
        base_class_mock._get_data_type = mock.MagicMock(return_value="data_type")
        base_class_mock._get_base_attributes = mock.MagicMock(return_value="meta_model_base_attributes")
        default_code_mock.return_value = "code"
        result = CodeInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "code"
        base_class_mock._get_data_type.assert_called_once_with("element_node")
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        default_code_mock.assert_called_once_with("meta_model_base_attributes", "data_type")

    def test_create_instance_raise_exeption(self):
        base_class_mock = mock.MagicMock(name="CodeInstantiator_class")
        base_class_mock._get_data_type.return_value = None
        with pytest.raises(TypeError) as error:
            CodeInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == DATA_TYPE_ERROR_MSG
