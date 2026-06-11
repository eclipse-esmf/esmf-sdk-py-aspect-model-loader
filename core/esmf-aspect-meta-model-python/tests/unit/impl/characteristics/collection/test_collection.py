"""DefaultCollection class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultCollection


class TestDefaultCollection:
    """DefaultCollection unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")
    characteristic_mock = mock.MagicMock(name="characteristic")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCollection._set_parent_element_on_child_element"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_init(self, super_mock, set_parent_element_on_child_element_mock):
        """Test DefaultCollection initialization."""
        result = DefaultCollection(self.meta_model_mock, self.data_type_mock, self.characteristic_mock)

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        assert result._element_characteristic == self.characteristic_mock
        set_parent_element_on_child_element_mock.assert_called_once()

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_set_parent_element_on_child_element_mock(self, _):
        """Test setting parent element on child characteristic."""
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, self.characteristic_mock)

        self.characteristic_mock.append_parent_element.assert_called_once_with(collection)

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_element_characteristic(self, _):
        """Test element_characteristic getter."""
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, self.characteristic_mock)
        result = collection.element_characteristic

        assert result == self.characteristic_mock

    def test_element_characteristic_set_value(self):
        """Test element_characteristic setter and side effects."""
        set_parent_element_on_child_element_mock = mock.MagicMock(name="set_parent_element_on_child_element")
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, None)
        collection._set_parent_element_on_child_element = set_parent_element_on_child_element_mock
        collection.element_characteristic = self.characteristic_mock
        result = collection.element_characteristic

        assert result == self.characteristic_mock
        assert collection._element_characteristic == self.characteristic_mock
        set_parent_element_on_child_element_mock.assert_called_once()

    def test_element_characteristic_set_value_raise_exception(self):
        """Test exception when setting element_characteristic to None."""
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, self.characteristic_mock)
        with pytest.raises(ValueError) as error:
            collection.element_characteristic = None

        assert str(error.value) == "Element characteristic cannot be None."
