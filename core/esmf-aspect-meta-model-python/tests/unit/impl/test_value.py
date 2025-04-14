"""DefaultValue class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultValue


class TestDefaultValue:
    """DefaultValue unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    @mock.patch("esmf_aspect_meta_model_python.impl.default_unit.BaseImpl.__init__")
    def test_init(self, super_mock):
        result = DefaultValue(self.meta_model_mock, "value")

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result.value == "value"
