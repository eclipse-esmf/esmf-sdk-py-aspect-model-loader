"""Property interface test suite."""

from unittest import mock

from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.property import AbstractProperty, Property


class AbstractPropertyInterface(AbstractProperty):
    """Abstract Property interface class for testing.

    Attributes:
        name (str): The name of the property.
    """

    def __init__(self, name):
        """Initialize the AbstractPropertyInterface.

        Args:
            name (str): The name of the property.
        """
        self.name = name

    def example_value(self):
        """Return an example value for the property."""
        pass

    def is_abstract(self):
        """Return whether the property is abstract."""
        pass

    def extends(self):
        """Return the property this property extends, if any."""
        pass

    def is_optional(self):
        """Return whether the property is optional."""
        pass

    def is_not_in_payload(self):
        """Return whether the property is not included in the payload."""
        pass

    def payload_name(self):
        """Return the payload name for the property."""
        pass

    @property
    def parent_elements(self):
        """Return the parent elements of the property."""
        return None

    @parent_elements.setter
    def parent_elements(self, elements):
        """Set the parent elements of the property."""
        pass

    def append_parent_element(self, element):
        """Append a parent element to the property."""
        pass

    def name(self):
        """Return the name of the property."""
        return self.name

    def preferred_names(self):
        """Return the preferred names for the property."""
        pass

    def descriptions(self):
        """Return the descriptions for the property."""
        pass

    def see(self):
        """Return the 'see' references for the property."""
        pass

    def urn(self):
        """Return the URN for the property."""
        pass

    def meta_model_version(self):
        """Return the meta model version for the property."""
        pass


class PropertyInterface(Property, AbstractPropertyInterface):
    """Property interface class for testing.

    Attributes:
        name (str): The name of the property.
        characteristic: The characteristic associated with the property.
    """

    def __init__(self, name, characteristic=None):
        """Initialize the PropertyInterface.

        Args:
            name (str): The name of the property.
            characteristic: The characteristic associated with the property (optional).
        """
        self.name = name
        self.characteristic = characteristic

    def characteristic(self):
        """Return the characteristic associated with the property."""
        pass


class TestAbstractProperty:
    """Abstract Property interface test suite."""

    def test_data_type(self):
        """Test that the data_type property returns None for AbstractPropertyInterface."""
        interface = AbstractPropertyInterface("name")
        result = interface.data_type

        assert result is None


class TestProperty:
    """Property interface test suite."""

    def test_data_type(self):
        """Test that the data_type property returns the correct value from the characteristic."""
        characteristic_mock = mock.MagicMock(name="characteristic")
        characteristic_mock.data_type = "data_type"
        interface = PropertyInterface("name", characteristic_mock)
        result = interface.data_type

        assert result == "data_type"

    def test_data_type_empty(self):
        """Test that the data_type property returns None when characteristic is None."""
        interface = PropertyInterface("name", characteristic=None)
        result = interface.data_type

        assert result is None

    def test_effective_characteristic_empty(self):
        """Test that effective_characteristic returns None when characteristic is not set."""
        interface = PropertyInterface("name")
        result = interface.effective_characteristic

        assert result is None

    @mock.patch("esmf_aspect_meta_model_python.base.property.isinstance")
    def test_effective_characteristic(self, isinstance_mock):
        """Test that effective_characteristic returns the base_characteristic when Trait is detected."""
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
