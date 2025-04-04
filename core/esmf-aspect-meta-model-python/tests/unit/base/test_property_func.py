"""Property Func interface test suite."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class TestPropertyFunc:
    """Property Func interface test suite."""

    def test_fget_name(self):
        callable_property_mock = mock.MagicMock(name="callable_property")
        callable_property_mock.fget.__name__ = "test_name"
        result = PropertyFunc.fget_name(callable_property_mock)

        assert result == "test_name"

    def test_fget_name_raises_attribute_error(self):
        with pytest.raises(AttributeError) as error:
            PropertyFunc.fget_name(None)

        assert str(error.value) == "Unable to execute fget.__name__ for this argument."

    def test_has_properties(self):
        class TestClass:
            def __init__(self, a, b):
                self._a = a
                self._b = b

            @property
            def a(self):
                return self._a

            @property
            def b(self):
                return self._b

        obj = TestClass("value_1", "value_2")
        result = PropertyFunc.has_properties(obj, TestClass.a, TestClass.b)

        assert result is True

    def test_has_properties_missing_property(self):
        class BaseTestClass:
            def __init__(self, a, b):
                self._a = a
                self._b = b

            @property
            def a(self):
                return self._a

            @property
            def b(self):
                return self._b

        class TestClass:
            def __init__(self, a, b):
                self._a = a
                self._b = b

            @property
            def a(self):
                return self._a

        obj = TestClass("value_1", "value_2")
        result = PropertyFunc.has_properties(obj, BaseTestClass.a, BaseTestClass.b)

        assert result is False
