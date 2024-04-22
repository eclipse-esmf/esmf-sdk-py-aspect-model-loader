"""DefaultAspect class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultAspect


class TestDefaultAspect:
    """DefaultAspect unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    property_mock = mock.MagicMock(name="property")
    operation_mock = mock.MagicMock(name="operation")
    event_mock = mock.MagicMock(name="event")
    is_collection_aspect = True

    @mock.patch("esmf_aspect_meta_model_python.impl.default_aspect.DefaultAspect._set_parent_element_on_child_elements")
    @mock.patch("esmf_aspect_meta_model_python.impl.default_aspect.BaseImpl.__init__")
    def test_init(self, super_mock, set_parent_element_on_child_elements_mock):
        result = DefaultAspect(
            self.meta_model_mock,
            [self.property_mock],
            [self.operation_mock],
            [self.event_mock],
            self.is_collection_aspect,
        )

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._properties == [self.property_mock]
        assert result._operations == [self.operation_mock]
        assert result._events == [self.event_mock]
        assert result._is_collection_aspect == self.is_collection_aspect
        set_parent_element_on_child_elements_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.impl.default_aspect.BaseImpl.__init__")
    def test_set_parent_element_on_child_elements(self, _):
        aspect = DefaultAspect(
            self.meta_model_mock,
            [self.property_mock],
            [self.operation_mock],
            [self.event_mock],
            self.is_collection_aspect,
        )

        self.property_mock.append_parent_element.assert_called_once_with(aspect)
        self.operation_mock.append_parent_element.assert_called_once_with(aspect)
        self.event_mock.append_parent_element.assert_called_once_with(aspect)

    @mock.patch("esmf_aspect_meta_model_python.impl.default_aspect.BaseImpl.__init__")
    def test_operations(self, _):
        aspect = DefaultAspect(
            self.meta_model_mock,
            [self.property_mock],
            [self.operation_mock],
            [self.event_mock],
            self.is_collection_aspect,
        )
        result = aspect.operations

        assert result == [self.operation_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.default_aspect.BaseImpl.__init__")
    def test_properties(self, _):
        aspect = DefaultAspect(
            self.meta_model_mock,
            [self.property_mock],
            [self.operation_mock],
            [self.event_mock],
            self.is_collection_aspect,
        )
        result = aspect.properties

        assert result == [self.property_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.default_aspect.BaseImpl.__init__")
    def test_events(self, _):
        aspect = DefaultAspect(
            self.meta_model_mock,
            [self.property_mock],
            [self.operation_mock],
            [self.event_mock],
            self.is_collection_aspect,
        )
        result = aspect.events

        assert result == [self.event_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.default_aspect.BaseImpl.__init__")
    def test_is_collection_aspect(self, _):
        aspect = DefaultAspect(
            self.meta_model_mock,
            [self.property_mock],
            [self.operation_mock],
            [self.event_mock],
            self.is_collection_aspect,
        )
        result = aspect.is_collection_aspect

        assert result == self.is_collection_aspect
