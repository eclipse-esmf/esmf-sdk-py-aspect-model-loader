"""DefaultUnit class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultUnit


class TestDefaultUnit:
    """DefaultUnit unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    symbol = "symbol"
    code = "code"
    reference_unit = "reference_unit"
    conversion_factor = "conversion_factor"
    quantity_kinds_mock = mock.MagicMock(name="quantity_kinds")

    @mock.patch("esmf_aspect_meta_model_python.impl.default_unit.DefaultUnit._set_parent_element_on_child_elements")
    @mock.patch("esmf_aspect_meta_model_python.impl.default_unit.BaseImpl.__init__")
    def test_init(self, super_mock, set_parent_element_on_child_elements_mock):
        result = DefaultUnit(
            self.meta_model_mock,
            self.symbol,
            self.code,
            self.reference_unit,
            self.conversion_factor,
            {self.quantity_kinds_mock},
        )

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._symbol == self.symbol
        assert result._code == self.code
        assert result._reference_unit == self.reference_unit
        assert result._conversion_factor == self.conversion_factor
        assert result._quantity_kinds == {self.quantity_kinds_mock}
        set_parent_element_on_child_elements_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_set_parent_element_on_child_elements_mock(self, _):
        quantity_kinds_mock = mock.MagicMock(name="quantity_kinds")
        unit = DefaultUnit(
            self.meta_model_mock,
            self.symbol,
            self.code,
            self.reference_unit,
            self.conversion_factor,
            {quantity_kinds_mock},
        )

        quantity_kinds_mock.append_parent_element.assert_called_once_with(unit)

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_symbol(self, _):
        unit = DefaultUnit(
            self.meta_model_mock,
            self.symbol,
            self.code,
            self.reference_unit,
            self.conversion_factor,
            {self.quantity_kinds_mock},
        )
        result = unit.symbol

        assert result == self.symbol

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_code(self, _):
        unit = DefaultUnit(
            self.meta_model_mock,
            self.symbol,
            self.code,
            self.reference_unit,
            self.conversion_factor,
            {self.quantity_kinds_mock},
        )
        result = unit.code

        assert result == self.code

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_reference_unit(self, _):
        unit = DefaultUnit(
            self.meta_model_mock,
            self.symbol,
            self.code,
            self.reference_unit,
            self.conversion_factor,
            {self.quantity_kinds_mock},
        )
        result = unit.reference_unit

        assert result == self.reference_unit

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_conversion_factor(self, _):
        unit = DefaultUnit(
            self.meta_model_mock,
            self.symbol,
            self.code,
            self.reference_unit,
            self.conversion_factor,
            {self.quantity_kinds_mock},
        )
        result = unit.conversion_factor

        assert result == self.conversion_factor

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_quantity_kinds(self, _):
        unit = DefaultUnit(
            self.meta_model_mock,
            self.symbol,
            self.code,
            self.reference_unit,
            self.conversion_factor,
            {self.quantity_kinds_mock},
        )
        result = unit.quantity_kinds

        assert result == {self.quantity_kinds_mock}
