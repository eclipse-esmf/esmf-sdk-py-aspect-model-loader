"""DefaultTrait class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultTrait


class TestDefaultTrait:
    """DefaultTrait unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    meta_model_mock.urn = "urn"
    characteristic_mock = mock.MagicMock(name="characteristic")
    characteristic_mock.data_type = "data_type"
    constraint_mock = mock.MagicMock(name="constraint")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_structured_value.DefaultCharacteristic.__init__"
    )
    def test_init(self, super_mock):
        result = DefaultTrait(self.meta_model_mock, self.characteristic_mock, [self.constraint_mock])

        super_mock.assert_called_once_with(self.meta_model_mock, "data_type")
        assert result._base_characteristic == self.characteristic_mock
        assert result._constraints == [self.constraint_mock]

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_structured_value.DefaultCharacteristic.__init__"
    )
    def test_base_characteristic(self, _):
        trait = DefaultTrait(self.meta_model_mock, self.characteristic_mock, [self.constraint_mock])
        result = trait.base_characteristic

        assert result == self.characteristic_mock

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_structured_value.DefaultCharacteristic.__init__"
    )
    def test_constraints(self, _):
        trait = DefaultTrait(self.meta_model_mock, self.characteristic_mock, [self.constraint_mock])
        result = trait.constraints

        assert result == [self.constraint_mock]
