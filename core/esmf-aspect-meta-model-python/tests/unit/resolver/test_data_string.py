"""Data string resolver test suit."""

from unittest import mock

from rdflib import RDF

from esmf_aspect_meta_model_python.resolver.data_string import DataStringResolver


class TestDataStringResolver:
    """Data string resolver test suit."""

    @mock.patch("esmf_aspect_meta_model_python.resolver.data_string.Graph")
    def test_read(self, rdf_graph_mock):
        graph_mock = mock.MagicMock(name="graph")
        rdf_graph_mock.return_value = graph_mock
        resolver = DataStringResolver()
        result = resolver.read("data_string")

        assert result == graph_mock
        graph_mock.parse.assert_called_once_with(data="data_string")

    @mock.patch("esmf_aspect_meta_model_python.resolver.data_string.SAMM")
    @mock.patch("esmf_aspect_meta_model_python.resolver.data_string.DataStringResolver.get_samm_version")
    def test_get_aspect_urn(self, get_samm_version_mock, samm_class_mock):
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_urn.return_value = "aspect_urn"
        samm_class_mock.return_value = samm_mock
        samm_class_mock.aspect = "aspect"
        get_samm_version_mock.return_value = "1.2.3"
        graph_mock = mock.MagicMock(mname="graph")
        graph_mock.value.return_value = "aspect_urn"
        resolver = DataStringResolver()
        resolver.graph = graph_mock
        result = resolver.get_aspect_urn()

        assert result == "aspect_urn"
        get_samm_version_mock.assert_called_once()
        samm_mock.get_urn.assert_called_once_with("aspect")
        graph_mock.value.assert_called_once_with(predicate=RDF.type, object="aspect_urn", any=False)
