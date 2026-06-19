"""ComplexType class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultComplexType


class TestComplexType:
    """ComplexType unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    property_mock = mock.MagicMock(name="property")

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_init(self, super_mock):
        """Test DefaultComplexType initialization."""
        property_mock = mock.MagicMock(name="property")
        DefaultComplexType._instances = {}
        DefaultComplexType.urn = "urn"
        result = DefaultComplexType(self.meta_model_mock, [property_mock], "extends_urn")

        super_mock.assert_called_once_with(self.meta_model_mock)
        property_mock.append_parent_element.assert_called_once_with(result)
        assert result._DefaultComplexType__properties == [property_mock]
        assert result._DefaultComplexType__extends_urn == "extends_urn"
        assert DefaultComplexType._instances == {"urn": result}

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_extend_no_instance(self, _):
        """Test extends property when no instance exists."""
        DefaultComplexType.urn = None
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], None)
        result = complex_type.extends

        assert result is None

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_extend(self, _):
        """Test extends property with existing instance."""
        DefaultComplexType.urn = None
        DefaultComplexType._instances = {"extends_urn": "instance"}
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.extends

        assert result == "instance"

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_extend_empty(self, _):
        """Test extends property when extends is None."""
        DefaultComplexType.urn = None
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], extends=None)
        result = complex_type.extends

        assert result is None

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_preferred_names_no_extends(self, _):
        """Test preferred_names property with no extends."""
        DefaultComplexType.urn = None
        DefaultComplexType._instances = {}
        DefaultComplexType._preferred_names = {"name": "instance"}
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.preferred_names

        assert result == {"name": "instance"}

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_preferred_names_with_extends(self, _):
        """Test preferred_names property with extends."""
        DefaultComplexType.urn = None
        complex_type_data_mock = mock.MagicMock(name="complex_type_data")
        complex_type_data_mock.preferred_names = {"preferred_name_1": "instance_1"}
        DefaultComplexType._instances = {"extends_urn": complex_type_data_mock}
        DefaultComplexType._preferred_names = {"preferred_name_2": "instance_2"}
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.preferred_names

        assert "preferred_name_1" in result
        assert result["preferred_name_1"] == "instance_1"
        assert "preferred_name_2" in result
        assert result["preferred_name_2"] == "instance_2"

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_descriptions_no_extends(self, _):
        """Test descriptions property with no extends."""
        DefaultComplexType.urn = None
        DefaultComplexType._instances = {}
        DefaultComplexType._descriptions = {"name": "description"}
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.descriptions

        assert result == {"name": "description"}

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_descriptions_with_extends(self, _):
        """Test descriptions property with extends."""
        DefaultComplexType.urn = None
        complex_type_data_mock = mock.MagicMock(name="complex_type_data")
        complex_type_data_mock.descriptions = {"name_1": "descriptions_1"}
        DefaultComplexType._instances = {"extends_urn": complex_type_data_mock}
        DefaultComplexType._descriptions = {"name_2": "descriptions_2"}
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.descriptions

        assert "name_1" in result
        assert result["name_1"] == "descriptions_1"
        assert "name_2" in result
        assert result["name_2"] == "descriptions_2"

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_see_no_extends(self, _):
        """Test see property with no extends."""
        DefaultComplexType.urn = None
        DefaultComplexType._instances = {}
        DefaultComplexType._see = ["see"]
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.see

        assert result == ["see"]

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_see_with_extends(self, _):
        """Test see property with extends."""
        DefaultComplexType.urn = None
        complex_type_data_mock = mock.MagicMock(name="complex_type_data")
        complex_type_data_mock.see = ["see_1"]
        DefaultComplexType._instances = {"extends_urn": complex_type_data_mock}
        DefaultComplexType._see = ["see_2"]
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.see

        assert sorted(result) == ["see_1", "see_2"]

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_all_properties_extends_urn_is_none(self, _):
        """Test all_properties when extends_urn is None."""
        DefaultComplexType.urn = None
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], None)
        result = complex_type.all_properties

        assert result == [self.property_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_all_properties_extends_urn_no_extends(self, _):
        """Test all_properties when extends_urn has no extends."""
        DefaultComplexType.urn = None
        DefaultComplexType._instances = {}
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.all_properties

        assert result == [self.property_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_all_properties_extends_urn_with_extends(self, _):
        """Test all_properties when extends_urn has extends."""
        DefaultComplexType.urn = None
        complex_type_data_mock = mock.MagicMock(name="complex_type_data")
        property_1_mock = mock.MagicMock(name="property_1")
        complex_type_data_mock.all_properties = [property_1_mock]
        DefaultComplexType._instances = {"extends_urn": complex_type_data_mock}
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], "extends_urn")
        result = complex_type.all_properties

        assert result == [self.property_mock, property_1_mock]

    @mock.patch("esmf_aspect_meta_model_python.impl.data_types.default_complex_type.BaseImpl.__init__")
    def test_properties(self, _):
        """Test properties getter."""
        DefaultComplexType.urn = None
        complex_type = DefaultComplexType(self.meta_model_mock, [self.property_mock], None)
        result = complex_type.properties

        assert result == [self.property_mock]
