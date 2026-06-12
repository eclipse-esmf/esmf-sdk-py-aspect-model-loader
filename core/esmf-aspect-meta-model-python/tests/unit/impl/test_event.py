"""DefaultEvent class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultEvent


class TestEvent:
    """DefaultEvent unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    property_mock = mock.MagicMock(name="property")

    @mock.patch("esmf_aspect_meta_model_python.impl.default_event.BaseImpl.__init__")
    def test_init(self, super_mock):
        """Test __init__ method."""
        result = DefaultEvent(self.meta_model_mock, [self.property_mock])

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._parameters == [self.property_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.default_event.BaseImpl.__init__")
    def test_parameters(self, _):
        """Test parameters property."""
        event = DefaultEvent(self.meta_model_mock, [self.property_mock])
        result = event.parameters

        assert result == [self.property_mock]
