"""DefaultCollection class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection import DefaultCollection


class TestDefaultCollection:
    """DefaultCollection unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")

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
        characteristic_mock = mock.MagicMock(name="characteristic")
        result = DefaultCollection(self.meta_model_mock, self.data_type_mock, characteristic_mock)

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        assert result._element_characteristic == characteristic_mock
        set_parent_element_on_child_element_mock.assert_called_once()

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_set_parent_element_on_child_element(self, _):
        """Test setting parent element on child characteristic."""
        characteristic_mock = mock.MagicMock(name="characteristic")
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, characteristic_mock)

        characteristic_mock.append_parent_element.assert_called_once_with(collection)

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_set_parent_element_on_child_element_no_element_characteristic(self, _):
        """Test setting parent element on child characteristic when no element_characteristic."""
        characteristic_mock = mock.MagicMock(name="characteristic")
        _ = DefaultCollection(self.meta_model_mock, self.data_type_mock, None)

        characteristic_mock.append_parent_element.assert_not_called()

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_element_characteristic(self, _):
        """Test element_characteristic getter."""
        characteristic_mock = mock.MagicMock(name="characteristic")
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, characteristic_mock)
        result = collection.element_characteristic

        assert result == characteristic_mock
