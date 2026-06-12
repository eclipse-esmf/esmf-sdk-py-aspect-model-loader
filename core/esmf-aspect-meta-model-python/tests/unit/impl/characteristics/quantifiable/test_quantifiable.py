"""DefaultQuantifiable class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl.characteristics.quantifiable.default_quantifiable import DefaultQuantifiable


class TestDefaultQuantifiable:
    """DefaultQuantifiable unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.quantifiable.default_quantifiable."
        "DefaultCharacteristic.__init__"
    )
    def test_init(self, super_mock):
        unit_mock = mock.MagicMock(name="unit")
        result = DefaultQuantifiable(self.meta_model_mock, self.data_type_mock, unit_mock)

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        assert result._unit == unit_mock
        unit_mock.append_parent_element.assert_called_once_with(result)

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.quantifiable.default_quantifiable."
        "DefaultCharacteristic.__init__"
    )
    def test_init_unit_empty(self, super_mock):
        result = DefaultQuantifiable(self.meta_model_mock, self.data_type_mock, unit=None)

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        assert result._unit is None

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_unit(self, _):
        unit_mock = mock.MagicMock(name="unit")
        quantifiable = DefaultQuantifiable(self.meta_model_mock, self.data_type_mock, unit_mock)
        result = quantifiable.unit

        assert result == unit_mock
