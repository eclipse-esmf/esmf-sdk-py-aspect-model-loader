"""BaseImpl class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.base.is_described import IsDescribed
from esmf_aspect_meta_model_python.impl import BaseImpl


def get_meta_model_mock():
    """Create a mock object for meta model base attributes.

    Returns:
        MagicMock: A mock object with meta model attributes set.
    """
    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    meta_model_mock.meta_model_version = "meta_model_version"
    meta_model_mock.urn = "urn"
    meta_model_mock.name = "name"
    meta_model_mock.preferred_names = "preferred_names"
    meta_model_mock.descriptions = "descriptions"
    meta_model_mock.see = "see"

    return meta_model_mock


class TestBaseImpl:
    """BaseImpl unit tests class."""

    meta_model_mock = get_meta_model_mock()

    def test_init(self):
        """Test BaseImpl initialization and attribute assignment."""
        result = BaseImpl(self.meta_model_mock)

        assert result._meta_model_version == "meta_model_version"
        assert result._urn == "urn"
        assert result._name == "name"
        assert result._preferred_names == "preferred_names"
        assert result._descriptions == "descriptions"
        assert result._see == "see"
        assert result._parent_elements is None

    def test_parent_elements_getter_none(self):
        """Test parent_elements returns None if not set."""
        base = BaseImpl(self.meta_model_mock)
        result = base.parent_elements

        assert result is None

    def test_parent_elements_getter_list(self):
        """Test parent_elements returns list after append."""
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(element_mock)
        result = base.parent_elements

        assert result == [element_mock]

    def test_parent_elements_setter_none(self):
        """Test setting parent_elements to non-list gives None."""
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.parent_elements = element_mock
        result = base.parent_elements

        assert result is None

    def test_parent_elements_setter_value(self):
        """Test setting parent_elements to a list replaces it."""
        base = BaseImpl(self.meta_model_mock)
        initial_element_mock = mock.MagicMock(name="init_element")
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(initial_element_mock)
        base.parent_elements = [element_mock]
        result = base.parent_elements

        assert result == [element_mock]

    def test_append_parent_element_no_parent_elements(self):
        """Test append_parent_element with no prior elements."""
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(element_mock)
        result = base._parent_elements

        assert result == [element_mock]

    def test_append_parent_element(self):
        """Test appending multiple parent elements."""
        base = BaseImpl(self.meta_model_mock)
        initial_element_mock = mock.MagicMock(name="init_element")
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(initial_element_mock)
        base.append_parent_element(element_mock)
        result = base.parent_elements

        assert result == [initial_element_mock, element_mock]

    def test_meta_model_version(self):
        """Test meta_model_version property."""
        base = BaseImpl(self.meta_model_mock)
        result = base.meta_model_version

        assert result == "meta_model_version"

    def test_preferred_names(self):
        """Test preferred_names property."""
        base = BaseImpl(self.meta_model_mock)
        result = base.preferred_names

        assert result == "preferred_names"

    def test_descriptions(self):
        """Test descriptions property."""
        base = BaseImpl(self.meta_model_mock)
        result = base.descriptions

        assert result == "descriptions"

    def test_see(self):
        """Test see property."""
        base = BaseImpl(self.meta_model_mock)
        result = base.see

        assert result == "see"

    def test_urn(self):
        """Test urn property."""
        base = BaseImpl(self.meta_model_mock)
        result = base.urn

        assert result == "urn"

    def test_name(self):
        """Test name property."""
        base = BaseImpl(self.meta_model_mock)
        result = base.name

        assert result == "name"

    def test_get_base_message(self):
        """Test _get_base_message output."""
        base = BaseImpl(self.meta_model_mock)
        result = base._get_base_message()

        assert result == "(BaseImpl)name"

    def test_prepare_attr_message_dict_value(self):
        """Test _prepare_attr_message with dict value."""
        value = {"attr_name": "attr_value"}
        result = BaseImpl._prepare_attr_message("name", value)

        assert result == "name: \n\t\tATTR_NAME: attr_value"

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.repr")
    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_attr_message_base_node_value(self, isinstance_mock, repr_mock):
        """Test _prepare_attr_message with BaseImpl value."""
        isinstance_mock.side_effect = (False, True)
        repr_mock.return_value = "value_repr"
        result = BaseImpl._prepare_attr_message("name", "value")

        assert result == "name: value_repr"
        isinstance_mock.assert_has_calls(
            [
                mock.call("value", dict),
                mock.call("value", BaseImpl),
            ]
        )
        repr_mock.assert_called_once_with("value")

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.str")
    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_attr_message_base_data_type_value(self, isinstance_mock, str_mock):
        """Test _prepare_attr_message with non-BaseImpl value."""
        isinstance_mock.side_effect = (False, False)
        str_mock.return_value = "class_name:\n\tvalue_name: value_repr"
        result = BaseImpl._prepare_attr_message("name", "value")

        assert result == "name: class_name:\n\t\tvalue_name: value_repr"
        isinstance_mock.assert_has_calls(
            [
                mock.call("value", dict),
                mock.call("value", BaseImpl),
            ]
        )
        str_mock.assert_called_once_with("value")

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_attr_message(self, isinstance_mock):
        """Test _prepare_attr_message with scalar value."""
        isinstance_mock.side_effect = (False, False)
        result = BaseImpl._prepare_attr_message("name", 1)

        assert result == "name: 1"
        isinstance_mock.assert_has_calls([mock.call(1, dict), mock.call(1, BaseImpl)])

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._prepare_attr_message")
    def test_get_scalar_attr_info(self, prepare_attr_message_mock):
        """Test _get_scalar_attr_info output."""
        prepare_attr_message_mock.return_value = "attr_message"
        base = BaseImpl(self.meta_model_mock)
        base.SCALAR_ATTR_NAMES = ["attr_name"]
        base.attr_name = "attr_value"
        result = base._get_scalar_attr_info()

        assert result == "\n\tattr_message"

    def test_get_scalar_attr_info_no_attr_value(self):
        """Test _get_scalar_attr_info output when attribute value is None."""
        base = BaseImpl(self.meta_model_mock)
        base.SCALAR_ATTR_NAMES = ["attr_name"]
        base.attr_name = None
        result = base._get_scalar_attr_info()

        assert result == ""

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_list_attr_message_attr_with_name(self, isinstance_mock):
        """Test _prepare_list_attr_message with IsDescribed value."""
        isinstance_mock.return_value = True
        value_mock = mock.MagicMock(name="element")
        value_mock.name = "value_name"
        result = BaseImpl._prepare_list_attr_message("name", [value_mock])

        assert result == "name:\n\t\tvalue_name"
        isinstance_mock.assert_called_once_with(value_mock, IsDescribed)

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_list_attr_message_scalar_attr(self, isinstance_mock):
        """Test _prepare_list_attr_message with scalar value."""
        isinstance_mock.return_value = False
        result = BaseImpl._prepare_list_attr_message("name", [1])

        assert result == "name:\n\t\t1"
        isinstance_mock.assert_called_once_with(1, IsDescribed)

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._prepare_list_attr_message")
    def test_get_list_attr_info(self, prepare_list_attr_message_mock):
        """Test _get_list_attr_info output."""
        prepare_list_attr_message_mock.return_value = "attr_message"
        base = BaseImpl(self.meta_model_mock)
        base.LIST_ATTR_NAMES = ["attr_name"]
        base.attr_name = "attr_value"
        result = base._get_list_attr_info()

        assert result == "\n\tattr_message"

    def test_get_list_attr_info_no_attr_value(self):
        """Test _get_list_attr_info output when attribute value is None."""
        base = BaseImpl(self.meta_model_mock)
        base.LIST_ATTR_NAMES = ["attr_name"]
        base.attr_name = None
        result = base._get_list_attr_info()

        assert result == ""

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._get_list_attr_info")
    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._get_scalar_attr_info")
    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._get_base_message")
    def test_str(self, get_base_message_mock, get_scalar_attr_info_mock, get_list_attr_info_mock):
        """Test __str__ output for BaseImpl."""
        get_base_message_mock.return_value = "base message"
        get_scalar_attr_info_mock.return_value = "\ncalar attributes info"
        get_list_attr_info_mock.return_value = "\nlist attributes info"
        base = BaseImpl(self.meta_model_mock)
        result = str(base)

        assert result == "base message\ncalar attributes info\nlist attributes info"

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_validate_attribute(self, isinstance_mock):
        """Test _validate_attribute with valid value."""
        isinstance_mock.side_effect = (True, True)
        attr_value_mock = mock.MagicMock(name="attr_value")
        attr_value_mock.urn = "urn:model#aspect"
        base = BaseImpl(self.meta_model_mock)
        base.REQUIRED_ATTRS = "attr_name"
        result = base._validate_attribute("attr_name", attr_value_mock)

        assert result is None
        attr_value_mock.validate.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_validate_attribute_no_required_attr(self, isinstance_mock):
        """Test _validate_attribute with no required attribute."""
        isinstance_mock.side_effect = (True, False)
        attr_value_mock = mock.MagicMock(name="attr_value")
        attr_value_mock.urn = "urn:model#aspect"
        base = BaseImpl(self.meta_model_mock)
        base.REQUIRED_ATTRS = ["other_attr_name"]
        result = base._validate_attribute("attr_name", attr_value_mock)

        assert result is None
        attr_value_mock.validate.assert_not_called()

    def test_validate_attribute_raise_exception(self):
        """Test _validate_attribute with missing required value."""
        base = BaseImpl(self.meta_model_mock)
        base.REQUIRED_ATTRS = "attr_name"
        with pytest.raises(ValueError) as error:
            base._validate_attribute("attr_name", None)

        assert str(error.value) == "BaseImpl is missing required attribute: attr_name. key: NoneType_attr_name: None"

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_validate_attribute_already_validated(self, isinstance_mock):
        """Test _validate_attribute with already validated value."""
        base = BaseImpl(self.meta_model_mock)
        attr_value_mock = mock.MagicMock(name="attr_value")
        attr_value_mock.urn = "urn:model#aspect"
        base._validating_attrs = {"urn:model#aspect"}
        result = base._validate_attribute("attr_name", attr_value_mock)

        assert result is None
        isinstance_mock.assert_called_once_with(attr_value_mock, BaseImpl)

    def test_validate(self):
        """Test validate method with valid attributes."""
        base = BaseImpl(self.meta_model_mock)
        base.SCALAR_ATTR_NAMES = ["scalar_attr"]
        base.LIST_ATTR_NAMES = ["list_attr"]
        base.scalar_attr = "scalar_value"
        base.list_attr = ["list_value"]
        validate_attribute_mock = mock.MagicMock(name="validate_attribute")
        base._validate_attribute = validate_attribute_mock
        result = base.validate()

        assert result is None
        validate_attribute_mock.assert_has_calls(
            [
                mock.call("scalar_attr", "scalar_value"),
                mock.call("list_attr", "list_value"),
            ]
        )
