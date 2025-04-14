"""DefaultCharacteristic class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultCharacteristic


class TestDefaultCharacteristic:
    """DefaultCharacteristic unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.BaseImpl.__init__")
    def test_init(self, super_mock, isinstance_mock):
        isinstance_mock.return_value = True
        result = DefaultCharacteristic(self.meta_model_mock, self.data_type_mock)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._data_type == self.data_type_mock
        self.data_type_mock.append_parent_element.assert_called_once_with(result)

    def test_init_raise_exception(self):
        with pytest.raises(ValueError) as error:
            DefaultCharacteristic(self.meta_model_mock, None)

        assert str(error.value) == "Attribute 'data_type' is required for Characteristic class."

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.BaseImpl.__init__")
    def test_data_type(self, _):
        characteristic = DefaultCharacteristic(self.meta_model_mock, self.data_type_mock)
        result = characteristic.data_type

        assert result == self.data_type_mock
