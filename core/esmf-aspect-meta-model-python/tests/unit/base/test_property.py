"""Property interface test suite."""

from unittest import mock

from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.property import Property


class PropertyInterface(Property):
    """Property interface class for testing."""

    def __init__(self, name, characteristic=None):
        self.name = name
        self.characteristic = characteristic

    def characteristic(self):
        pass

    def example_value(self):
        pass

    def is_abstract(self):
        pass

    def extends(self):
        pass

    def is_optional(self):
        pass

    def is_not_in_payload(self):
        pass

    def payload_name(self):
        pass

    @property
    def parent_elements(self):
        return None

    @parent_elements.setter
    def parent_elements(self, elements):
        pass

    def append_parent_element(self, element):
        pass

    def name(self):
        return self.name

    def preferred_names(self):
        pass

    def descriptions(self):
        pass

    def see(self):
        pass

    def urn(self):
        pass

    def meta_model_version(self):
        pass


class TestProperty:
    """Property interface test suite."""

    def test_effective_characteristic_empty(self):
        interface = PropertyInterface("name")
        result = interface.effective_characteristic

        assert result is None

    @mock.patch("esmf_aspect_meta_model_python.base.property.isinstance")
    def test_effective_characteristic(self, isinstance_mock):
        characteristic_mock = mock.MagicMock(name="characteristic")
        characteristic_mock.base_characteristic = "base_characteristic"
        isinstance_mock.side_effect = (True, False)
        interface = PropertyInterface("name", characteristic_mock)
        result = interface.effective_characteristic

        assert result == "base_characteristic"
        isinstance_mock.assert_has_calls(
            [
                mock.call(characteristic_mock, Trait),
                mock.call("base_characteristic", Trait),
            ]
        )
