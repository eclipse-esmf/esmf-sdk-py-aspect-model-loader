"""ScalarInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.scalar_instantiator import ScalarInstantiator


class TestScalarInstantiator:
    """ScalarInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.scalar_instantiator.DefaultScalar")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.scalar_instantiator.RdfHelper.to_python")
    def test_create_instance(self, to_python_mock, default_scalar_mock):
        base_class_mock = mock.MagicMock(name="ScalarInstantiator_class")
        base_class_mock._meta_model_version = "_meta_model_version"
        to_python_mock.return_value = "scalar_value"
        default_scalar_mock.return_value = "instance"
        result = ScalarInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        to_python_mock.assert_called_once_with("element_node")
        default_scalar_mock.assert_called_once_with("scalar_value", "_meta_model_version")

    def test_create_instance_raise_exception(self):
        base_class_mock = mock.MagicMock(name="ScalarInstantiator_class")
        with pytest.raises(ValueError) as error:
            ScalarInstantiator._create_instance(base_class_mock, None)

        assert str(error.value) == "Data Type is not specified"
