"""Scalar interface test suite."""

from esmf_aspect_meta_model_python.base.data_types.scalar import Scalar


class ScalarInterface(Scalar):
    """Scalar interface class for testing."""

    def __init__(self, urn):
        self._urn = urn

    @property
    def urn(self):
        return self._urn

    def meta_model_version(self):
        pass


class TestScalar:
    """Scalar interface test suite."""

    def test_resp(self):
        scalar = ScalarInterface("urn")
        result = repr(scalar)

        assert result == "ScalarInterface(urn)"
