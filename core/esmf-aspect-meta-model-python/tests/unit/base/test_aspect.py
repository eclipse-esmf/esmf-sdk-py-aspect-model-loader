"""Aspect interface test suite."""

from esmf_aspect_meta_model_python.base.aspect import Aspect


class AspectInterface(Aspect):
    """Aspect interface class for testing."""

    def __init__(self, name):
        self._name = name

    def urn(self):
        pass

    def meta_model_version(self):
        pass

    @property
    def name(self):
        return self._name

    def preferred_names(self):
        pass

    def descriptions(self):
        pass

    def see(self):
        pass

    def events(self):
        pass

    def operations(self):
        pass

    def properties(self):
        pass

    @property
    def parent_elements(self):
        return None

    @parent_elements.setter
    def parent_elements(self, elements):
        pass

    def append_parent_element(self, element):
        pass


class TestAspect:
    """Aspect interface test suite."""

    def test_is_collection_aspect(self):
        aspect = AspectInterface("name")
        result = aspect.is_collection_aspect

        assert result is False
