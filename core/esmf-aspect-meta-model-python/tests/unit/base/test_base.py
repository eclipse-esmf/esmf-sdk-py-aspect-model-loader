"""Base interface test suite."""

from esmf_aspect_meta_model_python.base.base import Base


class BaseInterface(Base):
    """Base interface class for testing."""

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

    @property
    def parent_elements(self):
        return None

    @parent_elements.setter
    def parent_elements(self, elements):
        pass

    def append_parent_element(self, element):
        pass


class TestBase:
    """Base interface test suite."""

    def test_resp(self):
        base = BaseInterface("name")
        result = repr(base)

        assert result == "BaseInterface(name)"
