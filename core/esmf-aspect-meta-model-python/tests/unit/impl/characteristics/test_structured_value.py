"""DefaultStructuredValue class unit tests suit."""

from unittest import mock

import pytest

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

    def test_deconstruction_rule_setter(self):
        characteristic = DefaultStructuredValue(
            self.meta_model_mock,
            self.data_type_mock,
            "deconstruction_rule",
            ["element"],
        )
        characteristic.deconstruction_rule = "new_deconstruction_rule"
        result = characteristic.deconstruction_rule

        assert result == "new_deconstruction_rule"

    def test_deconstruction_rule_setter_raise_exception(self):
        characteristic = DefaultStructuredValue(
            self.meta_model_mock, self.data_type_mock, "deconstruction_rule", ["element"]
        )
        with pytest.raises(ValueError) as error:
            characteristic.deconstruction_rule = None

        assert str(error.value) == "Deconstruction rule cannot be None."

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

    def test_elements_setter(self):
        characteristic = DefaultStructuredValue(
            self.meta_model_mock,
            self.data_type_mock,
            "deconstruction_rule",
            ["element"],
        )
        characteristic.elements = ["new_element"]
        result = characteristic.elements

        assert result == ["new_element"]
        assert characteristic._elements == ["new_element"]

    def test_elements_setter_raise_exception(self):
        characteristic = DefaultStructuredValue(
            self.meta_model_mock, self.data_type_mock, "deconstruction_rule", ["element"]
        )
        with pytest.raises(ValueError) as error:
            characteristic.elements = []

        assert str(error.value) == "Elements cannot be None or empty."
