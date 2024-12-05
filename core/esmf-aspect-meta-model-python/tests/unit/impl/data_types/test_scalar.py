"""Scalar class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultScalar


class TestScalar:
    """Scalar unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    def test_init(self):
        result = DefaultScalar("urn", self.meta_model_mock)

        assert result._urn == "urn"
        assert result._meta_model_version == self.meta_model_mock

    def test_urn(self):
        scalar = DefaultScalar("urn", self.meta_model_mock)
        result = scalar.urn

        assert result == "urn"

    def test_meta_model_version(self):
        scalar = DefaultScalar("urn", self.meta_model_mock)
        result = scalar.meta_model_version

        assert result == self.meta_model_mock

    def test_str(self):
        scalar = DefaultScalar("urn", "meta_model_version")
        result = str(scalar)

        assert result == "Scalar:\n\tmeta_model_version: meta_model_version\n\turn: urn"
