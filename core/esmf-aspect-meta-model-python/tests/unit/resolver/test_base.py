"""Base resolver test suit."""

from unittest import mock

import pytest

from rdflib import Graph

from esmf_aspect_meta_model_python.resolver.base import ResolverInterface


class ResolverTest(ResolverInterface):
    """Resolver interface test class."""

    def read(self, input_data):
        return Graph()

    def get_aspect_urn(self):
        return "aspect_urn"


class TestResolverInterface:
    """Resolver interface test suit."""

    def test_validate_samm_version_no_version(self):
        with pytest.raises(ValueError) as error:
            ResolverInterface._validate_samm_version("")

        assert str(error.value) == "SAMM version not found in the Graph."

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.SammUnitsGraph")
    def test_validate_samm_version_not_supported_version(self, samm_units_graph_mock):
        samm_units_graph_mock.SAMM_VERSION = "2"
        with pytest.raises(ValueError) as error:
            ResolverInterface._validate_samm_version("3")

        assert str(error.value) == "3 is not supported SAMM version."

    def test_get_samm_version_from_graph(self):
        graph_mock = mock.MagicMock(name="graph")
        graph_mock.namespace_manager.namespaces.return_value = [("samm", "path:model:0.1.2#")]
        resolver = ResolverTest()
        resolver.graph = graph_mock
        result = resolver._get_samm_version_from_graph()

        assert result == "0.1.2"
        graph_mock.namespace_manager.namespaces.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.resolver.base.ResolverInterface._validate_samm_version")
    @mock.patch("esmf_aspect_meta_model_python.resolver.base.ResolverInterface._get_samm_version_from_graph")
    def test_get_samm_version(self, get_samm_version_from_graph_mock, validate_samm_version_mock):
        get_samm_version_from_graph_mock.return_value = "version"
        resolver = ResolverTest()
        result = resolver.get_samm_version()

        assert result == "version"
        get_samm_version_from_graph_mock.assert_called_once()
        validate_samm_version_mock.assert_called_once_with("version")
        assert resolver.samm_version == "version"
