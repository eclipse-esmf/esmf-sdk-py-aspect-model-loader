"""DefaultEnumeration class unit tests suit."""

from unittest import mock

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
