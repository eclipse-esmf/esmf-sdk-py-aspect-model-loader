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
        """Test DefaultCharacteristic initialization."""
        isinstance_mock.return_value = True
        result = DefaultCharacteristic(self.meta_model_mock, self.data_type_mock)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._data_type == self.data_type_mock
        self.data_type_mock.append_parent_element.assert_called_once_with(result)

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.BaseImpl.__init__")
    def test_data_type(self, _):
        """Test data_type getter."""
        characteristic = DefaultCharacteristic(self.meta_model_mock, self.data_type_mock)
        result = characteristic.data_type

        assert result == self.data_type_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.isinstance")
    def test_data_type_set_value(self, isinstance_mock):
        """Test setting data_type to a complex type."""
        isinstance_mock.return_value = True
        characteristic = DefaultCharacteristic(self.meta_model_mock, data_type=None)
        characteristic.data_type = self.data_type_mock
        result = characteristic.data_type

        assert result == self.data_type_mock
        assert characteristic._data_type == self.data_type_mock
        assert self.data_type_mock.append_parent_element.call_count == 2
        self.data_type_mock.append_parent_element.assert_has_calls([mock.call(characteristic)])

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.isinstance")
    def test_data_type_set_value_not_complex_type(self, isinstance_mock):
        """Test setting data_type to a non-complex type."""
        isinstance_mock.return_value = False
        data_type_mock = mock.MagicMock(name="data_type")
        characteristic = DefaultCharacteristic(self.meta_model_mock, data_type=None)
        characteristic.data_type = data_type_mock
        result = characteristic.data_type

        assert result == data_type_mock
        assert characteristic._data_type == data_type_mock
        assert data_type_mock.append_parent_element.call_count == 0

    def test_data_type_set_value_raise_exception(self):
        """Test exception when setting data_type to None."""
        characteristic = DefaultCharacteristic(self.meta_model_mock, data_type=self.data_type_mock)
        with pytest.raises(ValueError) as error:
            characteristic.data_type = None

        assert str(error.value) == "Data type cannot be None."
