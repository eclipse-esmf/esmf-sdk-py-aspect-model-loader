"""Complex Type interface test suite."""

from esmf_aspect_meta_model_python.base.data_types.complex_type import ComplexType


class ComplexTypeInterface(ComplexType):
    """ComplexType interface class for testing."""

    def name(self):
        pass

    def preferred_names(self):
        pass

    def descriptions(self):
        pass

    def see(self):
        pass

    def meta_model_version(self):
        pass

    def urn(self):
        pass

    def properties(self):
        pass

    def parent_elements(self):
        pass

    def append_parent_element(self, element):
        pass

    def all_properties(self):
        pass

    def extends(self):
        pass


class TestComplexType:
    """ComplexType interface test suite."""

    def test_is_abstract_entity(self):
        abstract_entity = ComplexTypeInterface()
        result = abstract_entity.is_abstract_entity

        assert result is False
