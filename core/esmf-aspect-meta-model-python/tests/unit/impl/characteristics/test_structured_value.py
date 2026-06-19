"""DefaultStructuredValue class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultStructuredValue


class TestDefaultStructuredValue:
    """DefaultStructuredValue unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_structured_value.DefaultCharacteristic.__init__"
    )
    def test_init(self, super_mock):
        result = DefaultStructuredValue(self.meta_model_mock, self.data_type_mock, "deconstruction_rule", ["element"])

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        assert result._deconstruction_rule == "deconstruction_rule"
        assert result._elements == ["element"]

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_structured_value.DefaultCharacteristic.__init__"
    )
    def test_deconstruction_rule(self, _):
        characteristic = DefaultStructuredValue(
            self.meta_model_mock, self.data_type_mock, "deconstruction_rule", ["element"]
        )
        result = characteristic.deconstruction_rule

        assert result == "deconstruction_rule"

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_structured_value.DefaultCharacteristic.__init__"
    )
    def test_elements(self, _):
        characteristic = DefaultStructuredValue(
            self.meta_model_mock,
            self.data_type_mock,
            "deconstruction_rule",
            ["element"],
        )
        result = characteristic.elements

        assert result == ["element"]
