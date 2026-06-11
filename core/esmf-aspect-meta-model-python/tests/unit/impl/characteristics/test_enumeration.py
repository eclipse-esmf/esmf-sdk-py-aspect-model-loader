"""DefaultEnumeration class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultEnumeration


class TestDefaultEnumeration:
    """DefaultEnumeration unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_enumeration.DefaultCharacteristic.__init__")
    def test_init(self, super_mock):
        """Test DefaultEnumeration initialization."""
        result = DefaultEnumeration(self.meta_model_mock, self.data_type_mock, ["value"])

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        assert result._values == ["value"]

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.DefaultCharacteristic.__init__"
    )
    def test_values(self, _):
        """Test values getter."""
        characteristic = DefaultEnumeration(self.meta_model_mock, self.data_type_mock, ["value"])
        result = characteristic.values

        assert result == ["value"]

    def test_values_setter(self):
        """Test values setter with valid input."""
        characteristic = DefaultEnumeration(self.meta_model_mock, self.data_type_mock, ["value"])
        characteristic.values = ["new_value"]
        result = characteristic.values

        assert result == ["new_value"]
        assert characteristic._values == ["new_value"]

    def test_values_setter_raise_exception(self):
        """Test exception when setting values to None."""
        characteristic = DefaultEnumeration(self.meta_model_mock, self.data_type_mock, ["value"])
        with pytest.raises(ValueError) as error:
            characteristic.values = None

        assert str(error.value) == "Values cannot be None."
