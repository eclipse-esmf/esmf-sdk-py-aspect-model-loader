"""DefaultProperty class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultAbstractProperty, DefaultProperty


class TestDefaultAbstractProperty:
    """DefaultAbstractProperty unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    elements_factory = mock.MagicMock(name="elements_factory")
    graph_node = mock.MagicMock(name="graph_node")
    example_value = "example_value"
    property_mock = mock.MagicMock(name="property")
    abstract = True
    optional = True
    not_in_payload = True
    payload_name = "payload_name"

    def _get_property_class(self):
        """
        Helper method to instantiate DefaultAbstractProperty with test parameters.

        Returns:
            DefaultAbstractProperty: Instance with preset test parameters.
        """
        return DefaultAbstractProperty(
            meta_model_base_attributes=self.meta_model_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )

    @mock.patch("esmf_aspect_meta_model_python.impl.default_property.BaseImpl.__init__")
    def test_init(self, super_mock):
        """Test DefaultAbstractProperty initialization and assignments."""
        result = self._get_property_class()

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._example_value == self.example_value
        assert result._is_abstract == self.abstract
        assert result._extends == self.property_mock
        assert result._optional == self.optional
        assert result._not_in_payload == self.not_in_payload
        assert result._payload_name == self.payload_name

    def test_example_value(self):
        """Test the example_value property of DefaultAbstractProperty."""
        property_cls = self._get_property_class()
        result = property_cls.example_value

        assert result == self.example_value

    def test_is_abstract(self):
        """Test the is_abstract property of DefaultAbstractProperty."""
        property_cls = self._get_property_class()
        result = property_cls.is_abstract

        assert result == self.abstract

    def test_extends(self):
        """Test the extends property of DefaultAbstractProperty."""
        property_cls = self._get_property_class()
        result = property_cls.extends

        assert result == self.property_mock

    def test_is_optional(self):
        """Test the is_optional property of DefaultAbstractProperty."""
        property_cls = self._get_property_class()
        result = property_cls.is_optional

        assert result == self.optional

    def test_is_not_in_payload(self):
        """Test the is_not_in_payload property of DefaultAbstractProperty."""
        property_cls = self._get_property_class()
        result = property_cls.is_not_in_payload

        assert result == self.not_in_payload

    def test_payload_name(self):
        """Test the payload_name property of DefaultAbstractProperty."""
        property_cls = self._get_property_class()
        result = property_cls.payload_name

        assert result == self.payload_name

    def test_preferred_names_no_extends(self):
        """Test preferred_names property when there is no extends property."""
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._preferred_names = "preferred_names"
        result = property_cls.preferred_names

        assert result == "preferred_names"

    def test_preferred_names_extends(self):
        """Test preferred_names property when there is an extends property."""
        property_mock = mock.MagicMock(name="property")
        property_mock.preferred_names = {"extend_property_preferred_names": "preferred_names"}
        property_cls = self._get_property_class()
        property_cls._preferred_names = {"base_preferred_names": "preferred_names"}
        property_cls._extends = property_mock
        result = property_cls.preferred_names

        assert "base_preferred_names" in result
        assert result["base_preferred_names"] == "preferred_names"
        assert "extend_property_preferred_names" in result
        assert result["extend_property_preferred_names"] == "preferred_names"

    def test_descriptions_no_extends(self):
        """Test descriptions property when there is no extends property."""
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._descriptions = "descriptions"
        result = property_cls.descriptions

        assert result == "descriptions"

    def test_descriptions_extends(self):
        """Test descriptions property when there is an extends property."""
        property_mock = mock.MagicMock(name="property")
        property_mock.descriptions = {"extend_property_descriptions": "descriptions"}
        property_cls = self._get_property_class()
        property_cls._extends = property_mock
        property_cls._descriptions = {"base_descriptions": "descriptions"}
        result = property_cls.descriptions

        assert "base_descriptions" in result
        assert result["base_descriptions"] == "descriptions"
        assert "extend_property_descriptions" in result
        assert result["extend_property_descriptions"] == "descriptions"

    def test_see_no_extends(self):
        """Test see property when there is no extends property."""
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._see = "see"
        result = property_cls.see

        assert result == "see"

    def test_see_extends(self):
        """Test see property when there is an extends property."""
        property_mock = mock.MagicMock(name="property")
        property_mock.see = ["extend_property_see"]
        property_cls = self._get_property_class()
        property_cls._extends = property_mock
        property_cls._see = ["base_see"]
        result = property_cls.see

        assert result == ["base_see", "extend_property_see"]


class TestDefaultProperty:
    """DefaultProperty unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    elements_factory = mock.MagicMock(name="elements_factory")
    graph_node = mock.MagicMock(name="graph_node")
    characteristic_mock = mock.MagicMock(name="characteristic")
    example_value = "example_value"
    property_mock = mock.MagicMock(name="property")
    abstract = True
    optional = True
    not_in_payload = True
    payload_name = "payload_name"

    def _get_property_class(self):
        """
        Helper method to instantiate DefaultProperty with test parameters.

        Returns:
            DefaultProperty: Instance with preset test parameters.
        """
        return DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )

    @mock.patch("esmf_aspect_meta_model_python.impl.default_property.BaseImpl.__init__")
    def test_init(self, super_mock):
        """Test DefaultProperty initialization and assignments."""
        characteristic_mock = mock.MagicMock(name="characteristic")
        result = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )

        super_mock.assert_called_once_with(self.meta_model_mock)
        characteristic_mock.append_parent_element.assert_called_once_with(result)
        assert result._characteristic == characteristic_mock
        assert result._example_value == self.example_value
        assert result._is_abstract == self.abstract
        assert result._extends == self.property_mock
        assert result._optional == self.optional
        assert result._not_in_payload == self.not_in_payload
        assert result._payload_name == self.payload_name

    def test_set_characteristic(self):
        """Test setting the characteristic and parent element assignment."""
        property_cls = self._get_property_class()

        assert self.characteristic_mock.append_parent_element.called
        self.characteristic_mock.append_parent_element.has_call(mock.call(property_cls))

    def test_set_characteristic_no_call_append_parent_element(self):
        """Test setting the characteristic and parent element assignment."""
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=None,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )

        assert property_cls._characteristic is None

    def test_characteristic(self):
        """Test the characteristic property of DefaultProperty."""
        property_cls = self._get_property_class()
        result = property_cls.characteristic

        assert result == self.characteristic_mock

    def test_characteristic_setter(self):
        """Test setting the characteristic and parent element assignment."""
        set_characteristic_mock = mock.MagicMock(name="set_characteristic")
        property_cls = self._get_property_class()
        property_cls._set_characteristic = set_characteristic_mock
        property_cls.characteristic = "characteristic"

        set_characteristic_mock.assert_called_once_with("characteristic")

    def test_characteristic_setter_raise_exception(self):
        """Test exception when setting characteristic to None."""
        property_cls = self._get_property_class()
        with pytest.raises(ValueError) as error:
            property_cls.characteristic = None

        assert str(error.value) == "Property must have a characteristic."

    def test_example_value(self):
        """Test the example_value property of DefaultProperty."""
        property_cls = self._get_property_class()
        result = property_cls.example_value

        assert result == self.example_value

    def test_is_abstract(self):
        """Test the is_abstract property of DefaultProperty."""
        property_cls = self._get_property_class()
        result = property_cls.is_abstract

        assert result == self.abstract

    def test_extends(self):
        """Test the extends property of DefaultProperty."""
        property_cls = self._get_property_class()
        result = property_cls.extends

        assert result == self.property_mock

    def test_is_optional(self):
        """Test the is_optional property of DefaultProperty."""
        property_cls = self._get_property_class()
        result = property_cls.is_optional

        assert result == self.optional

    def test_is_not_in_payload(self):
        """Test the is_not_in_payload property of DefaultProperty."""
        property_cls = self._get_property_class()
        result = property_cls.is_not_in_payload

        assert result == self.not_in_payload

    def test_payload_name(self):
        """Test the payload_name property of DefaultProperty."""
        property_cls = self._get_property_class()
        result = property_cls.payload_name

        assert result == self.payload_name

    def test_preferred_names_no_extends(self):
        """Test preferred_names property when there is no extends property."""
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._preferred_names = "preferred_names"
        result = property_cls.preferred_names

        assert result == "preferred_names"

    def test_preferred_names_extends(self):
        """Test preferred_names property when there is an extends property."""
        property_mock = mock.MagicMock(name="property")
        property_mock.preferred_names = {"extend_property_preferred_names": "preferred_names"}
        property_cls = self._get_property_class()
        property_cls._preferred_names = {"base_preferred_names": "preferred_names"}
        property_cls._extends = property_mock
        result = property_cls.preferred_names

        assert "base_preferred_names" in result
        assert result["base_preferred_names"] == "preferred_names"
        assert "extend_property_preferred_names" in result
        assert result["extend_property_preferred_names"] == "preferred_names"

    def test_descriptions_no_extends(self):
        """Test descriptions property when there is no extends property."""
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._descriptions = "descriptions"
        result = property_cls.descriptions

        assert result == "descriptions"

    def test_descriptions_extends(self):
        """Test descriptions property when there is an extends property."""
        property_mock = mock.MagicMock(name="property")
        property_mock.descriptions = {"extend_property_descriptions": "descriptions"}
        property_cls = self._get_property_class()
        property_cls._extends = property_mock
        property_cls._descriptions = {"base_descriptions": "descriptions"}
        result = property_cls.descriptions

        assert "base_descriptions" in result
        assert result["base_descriptions"] == "descriptions"
        assert "extend_property_descriptions" in result
        assert result["extend_property_descriptions"] == "descriptions"

    def test_see_no_extends(self):
        """Test see property when there is no extends property."""
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._see = "see"
        result = property_cls.see

        assert result == "see"

    def test_see_extends(self):
        """Test see property when there is an extends property."""
        property_mock = mock.MagicMock(name="property")
        property_mock.see = ["extend_property_see"]
        property_cls = self._get_property_class()
        property_cls._extends = property_mock
        property_cls._see = ["base_see"]
        result = property_cls.see

        assert result == ["base_see", "extend_property_see"]
