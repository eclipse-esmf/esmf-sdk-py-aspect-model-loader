"""DefaultEnumeration class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultState


class TestDefaultState:
    """DefaultState unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_state.DefaultEnumeration.__init__")
    def test_init(self, super_mock):
        """Test DefaultState initialization."""
        result = DefaultState(self.meta_model_mock, self.data_type_mock, ["value"], "default_value")

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock, ["value"])
        assert result._default_value == "default_value"

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_state.DefaultEnumeration.__init__")
    def test_default_value(self, _):
        """Test default_value getter."""
        characteristic = DefaultState(self.meta_model_mock, self.data_type_mock, ["value"], "default_value")
        result = characteristic.default_value

        assert result == "default_value"
