"""BaseElement class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.base.is_described import IsDescribed
from esmf_aspect_meta_model_python.impl import BaseImpl


def get_meta_model_mock():
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
        result = BaseImpl(self.meta_model_mock)

        assert result._meta_model_version == "meta_model_version"
        assert result._urn == "urn"
        assert result._name == "name"
        assert result._preferred_names == "preferred_names"
        assert result._descriptions == "descriptions"
        assert result._see == "see"
        assert result._parent_elements is None

    def test_parent_elements_getter_none(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.parent_elements

        assert result is None

    def test_parent_elements_getter_list(self):
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(element_mock)
        result = base.parent_elements

        assert result == [element_mock]

    def test_parent_elements_setter_none(self):
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.parent_elements = element_mock
        result = base.parent_elements

        assert result is None

    def test_parent_elements_setter_value(self):
        base = BaseImpl(self.meta_model_mock)
        initial_element_mock = mock.MagicMock(name="init_element")
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(initial_element_mock)
        base.parent_elements = [element_mock]
        result = base.parent_elements

        assert result == [element_mock]

    def test_append_parent_element_no_parent_elements(self):
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(element_mock)
        result = base._parent_elements

        assert result == [element_mock]

    def test_append_parent_element(self):
        base = BaseImpl(self.meta_model_mock)
        initial_element_mock = mock.MagicMock(name="init_element")
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(initial_element_mock)
        base.append_parent_element(element_mock)
        result = base.parent_elements

        assert result == [initial_element_mock, element_mock]

    def test_meta_model_version(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.meta_model_version

        assert result == "meta_model_version"

    def test_preferred_names(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.preferred_names

        assert result == "preferred_names"

    def test_descriptions(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.descriptions

        assert result == "descriptions"

    def test_see(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.see

        assert result == "see"

    def test_urn(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.urn

        assert result == "urn"

    def test_name(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.name

        assert result == "name"

    def test_get_base_message(self):
        base = BaseImpl(self.meta_model_mock)
        result = base._get_base_message()

        assert result == "(BaseImpl)name"

    def test_prepare_attr_message_dict_value(self):
        value = {"attr_name": "attr_value"}
        result = BaseImpl._prepare_attr_message("name", value)

        assert result == "name: \n\t\tATTR_NAME: attr_value"

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.repr")
    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_attr_message_base_node_value(self, isinstance_mock, repr_mock):
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
        isinstance_mock.side_effect = (False, False)
        result = BaseImpl._prepare_attr_message("name", 1)

        assert result == "name: 1"
        isinstance_mock.assert_has_calls([mock.call(1, dict), mock.call(1, BaseImpl)])

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._prepare_attr_message")
    def test_get_scalar_attr_info(self, prepare_attr_message_mock):
        prepare_attr_message_mock.return_value = "attr_message"
        base = BaseImpl(self.meta_model_mock)
        base.SCALAR_ATTR_NAMES = ["attr_name"]
        base.attr_name = "attr_value"
        result = base._get_scalar_attr_info()

        assert result == "\n\tattr_message"

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_list_attr_message_attr_with_name(self, isinstance_mock):
        isinstance_mock.return_value = True
        value_mock = mock.MagicMock(name="element")
        value_mock.name = "value_name"
        result = BaseImpl._prepare_list_attr_message("name", [value_mock])

        assert result == "name:\n\t\tvalue_name"
        isinstance_mock.assert_called_once_with(value_mock, IsDescribed)

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.isinstance")
    def test_prepare_list_attr_message_scalar_attr(self, isinstance_mock):
        isinstance_mock.return_value = False
        result = BaseImpl._prepare_list_attr_message("name", [1])

        assert result == "name:\n\t\t1"
        isinstance_mock.assert_called_once_with(1, IsDescribed)

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._prepare_list_attr_message")
    def test_get_list_attr_info(self, prepare_list_attr_message_mock):
        prepare_list_attr_message_mock.return_value = "attr_message"
        base = BaseImpl(self.meta_model_mock)
        base.LIST_ATTR_NAMES = ["attr_name"]
        base.attr_name = "attr_value"
        result = base._get_list_attr_info()

        assert result == "\n\tattr_message"

    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._get_list_attr_info")
    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._get_scalar_attr_info")
    @mock.patch("esmf_aspect_meta_model_python.impl.base_impl.BaseImpl._get_base_message")
    def test_str(self, get_base_message_mock, get_scalar_attr_info_mock, get_list_attr_info_mock):
        get_base_message_mock.return_value = "base message"
        get_scalar_attr_info_mock.return_value = "\ncalar attributes info"
        get_list_attr_info_mock.return_value = "\nlist attributes info"
        base = BaseImpl(self.meta_model_mock)
        result = str(base)

        assert result == "base message\ncalar attributes info\nlist attributes info"
