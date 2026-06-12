"""DefaultAbstractEntity class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultAbstractEntity


class TestDefaultAbstractEntity:
    """DefaultAbstractEntity unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    property_mock = mock.MagicMock(name="property")

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_abstract_entity.DefaultComplexType.__init__")
    def test_init(self, super_mock):
        result = DefaultAbstractEntity(self.meta_model_mock, [self.property_mock], "extends", ["extending_element"])

        super_mock.assert_called_once_with(self.meta_model_mock, [self.property_mock], "extends")
        assert result._DefaultAbstractEntity__extending_elements == ["extending_element"]

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_abstract_entity.DefaultComplexType")
    def test_extending_elements(self, default_complex_type_mock):
        default_complex_type_mock._instances = {"extending_element": "extending_element_instance"}
        abstract_entity = DefaultAbstractEntity(
            self.meta_model_mock, [self.property_mock], "extends", ["extending_element", "extending_element_2"]
        )
        result = abstract_entity.extending_elements

        assert result == ["extending_element_instance"]
