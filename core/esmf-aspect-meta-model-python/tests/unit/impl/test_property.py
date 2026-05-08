"""DefaultProperty class unit tests suit."""

from unittest import mock

# from esmf_aspect_meta_model_python.impl import DefaultBlankProperty, DefaultProperty, DefaultPropertyWithExtends
from esmf_aspect_meta_model_python.impl import DefaultProperty
from esmf_aspect_meta_model_python.loader.instantiator.property_instantiator import PropertyInstantiator
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


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
        result = self._get_property_class()

        super_mock.assert_called_once_with(self.meta_model_mock)
        self.characteristic_mock.append_parent_element.assert_called_once_with(result)
        assert result._characteristic == self.characteristic_mock
        assert result._example_value == self.example_value
        assert result._is_abstract == self.abstract
        assert result._extends == self.property_mock
        assert result._optional == self.optional
        assert result._not_in_payload == self.not_in_payload
        assert result._payload_name == self.payload_name

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_set_characteristic(self, _):
        property_cls = self._get_property_class()

        assert self.characteristic_mock.append_parent_element.called
        self.characteristic_mock.append_parent_element.has_call(mock.call(property_cls))

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_characteristic(self, _):
        property_cls = self._get_property_class()
        result = property_cls.characteristic

        assert result == self.characteristic_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_example_value(self, _):
        property_cls = self._get_property_class()
        result = property_cls.example_value

        assert result == self.example_value

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_is_abstract(self, _):
        property_cls = self._get_property_class()
        result = property_cls.is_abstract

        assert result == self.abstract

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_extends(self, _):
        property_cls = self._get_property_class()
        result = property_cls.extends

        assert result == self.property_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_is_optional(self, _):
        property_cls = self._get_property_class()
        result = property_cls.is_optional

        assert result == self.optional

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_is_not_in_payload(self, _):
        property_cls = self._get_property_class()
        result = property_cls.is_not_in_payload

        assert result == self.not_in_payload

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_payload_name(self, _):
        property_cls = self._get_property_class()
        result = property_cls.payload_name

        assert result == self.payload_name

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_preferred_names_no_extends(self, _):
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._preferred_names = "preferred_names"
        result = property_cls.preferred_names

        assert result == "preferred_names"

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_preferred_names_extends(self, _):
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

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_descriptions_no_extends(self, _):
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._descriptions = "descriptions"
        result = property_cls.descriptions

        assert result == "descriptions"

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_descriptions_extends(self, _):
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

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_see_no_extends(self, _):
        property_cls = self._get_property_class()
        property_cls._extends = None
        property_cls._see = "see"
        result = property_cls.see

        assert result == "see"

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_see_extends(self, _):
        property_mock = mock.MagicMock(name="property")
        property_mock.see = ["extend_property_see"]
        property_cls = self._get_property_class()
        property_cls._extends = property_mock
        property_cls._see = ["base_see"]
        result = property_cls.see

        assert result == ["base_see", "extend_property_see"]