"""SAMM Graph test suite."""

from unittest import mock

import pytest

from rdflib import RDF

from esmf_aspect_meta_model_python.loader.samm_graph import SAMMGraph


class TestSAMMGraph:
    """SAMM Graph test suite."""

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_init(self, populate_with_meta_data_mock):
        result = SAMMGraph("graph", "cache")

        assert result._graph == "graph"
        assert result._cache == "cache"
        assert result._samm_version == ""
        populate_with_meta_data_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_get_rdf_graph(self, _):
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph.get_rdf_graph()

        assert result == "graph"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_get_samm_version_from_graph(self, _):
        graph_mock = mock.MagicMock(name="graph")
        namespace_manager_mock = mock.MagicMock(name="namespace_manager")
        namespace_manager_mock.namespaces.return_value = [
            ("prefix", "some_link"),
            ("", "namespace"),
            ("samm", "namespace:path:to:model:3.2.1#"),
        ]
        graph_mock.namespace_manager = namespace_manager_mock
        samm_graph = SAMMGraph(graph_mock, "cache")
        result = samm_graph._get_samm_version_from_graph()

        assert result == "3.2.1"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_samm_version_from_graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_get_samm_version_raise_error(self, _, get_samm_version_from_graph_mock):
        get_samm_version_from_graph_mock.return_value = ""
        samm_graph = SAMMGraph("graph", "cache")
        with pytest.raises(ValueError) as error:
            samm_graph.get_samm_version()

        assert str(error.value) == "SAMM version not found in the Graph."
        get_samm_version_from_graph_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_samm_version_from_graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_get_samm_version(self, _, get_samm_version_from_graph_mock):
        get_samm_version_from_graph_mock.return_value = "1.2.3"
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph.get_samm_version()

        assert result is None
        assert samm_graph._samm_version == "1.2.3"
        get_samm_version_from_graph_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.AspectMetaModelResolver")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_samm_version")
    def test_populate_with_meta_data(self, get_samm_version_mock, aspect_meta_model_resolver_mock):
        meta_model_reader_mock = mock.MagicMock(name="meta_model_reader")
        aspect_meta_model_resolver_mock.return_value = meta_model_reader_mock
        _ = SAMMGraph("graph", "cache")

        get_samm_version_mock.assert_called_once()
        aspect_meta_model_resolver_mock.assert_called_once()
        meta_model_reader_mock.parse.assert_called_once_with("graph", "")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_prepare_graph(self, populate_with_meta_data_mock):
        _ = SAMMGraph(cache="cache")

        populate_with_meta_data_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMM")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_get_aspect_nodes_from_graph(self, _, rdf_graph_mock, samm_mock):
        rdf_graph_mock.return_value = rdf_graph_mock
        rdf_graph_mock.subjects.return_value = ["subject_1", "subject_2"]
        samm_mock.return_value = samm_mock
        samm_mock.aspect = "aspect"
        samm_mock.get_urn.return_value = "aspect_urn"
        samm_graph = SAMMGraph(cache="cache")
        samm_graph._samm_version = "1.2.3"
        result = samm_graph.get_aspect_nodes_from_graph()

        assert result == ["subject_1", "subject_2"]
        samm_mock.assert_called_once_with("1.2.3")
        samm_mock.get_urn.assert_called_once_with("aspect")
        rdf_graph_mock.assert_called_once()
        rdf_graph_mock.subjects.assert_called_once_with(predicate=RDF.type, object="aspect_urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.URIRef")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_get_base_nodes_with_aspect_urn(self, _, isinstance_mock, uri_ref_mock):
        isinstance_mock.return_value = False
        uri_ref_mock.return_value = "aspect_uri_ref"
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph.get_base_nodes("aspect_urn")

        assert result == ["aspect_uri_ref"]
        isinstance_mock.assert_called_once_with("aspect_urn", uri_ref_mock)
        uri_ref_mock.assert_called_once_with("aspect_urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_aspect_nodes_from_graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_get_base_nodes_no_aspect_urn(self, _, get_nodes_from_graph_mock):
        get_nodes_from_graph_mock.return_value = ["base_node"]
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph.get_base_nodes()

        assert result == ["base_node"]
        get_nodes_from_graph_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.ModelElementFactory")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_base_nodes")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_to_python(self, _, get_base_nodes_mock, model_element_factory_mock):
        get_base_nodes_mock.return_value = "base_nodes"
        model_element_factory_mock.return_value = model_element_factory_mock
        model_element_factory_mock.create_all_graph_elements.return_value = ["aspect_elements"]
        samm_graph = SAMMGraph("graph", "cache")
        samm_graph._samm_version = "samm_version"
        result = samm_graph.to_python("aspect_urn")

        assert result == ["aspect_elements"]
        get_base_nodes_mock.assert_called_once_with("aspect_urn")
        model_element_factory_mock.assert_called_once_with("samm_version", "graph", "cache")
        model_element_factory_mock.create_all_graph_elements.assert_called_once_with("base_nodes")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.DefaultElementCache")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_find_by_name(self, _, default_element_cache_mock):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_name.return_value = "graph_node"
        default_element_cache_mock.return_value = cache_mock
        samm_graph = SAMMGraph("graph")
        result = samm_graph.find_by_name("element_name")

        assert result == "graph_node"
        cache_mock.get_by_name.assert_called_once_with("element_name")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.DefaultElementCache")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_find_by_urn(self, _, default_element_cache_mock):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_urn.return_value = "graph_node"
        default_element_cache_mock.return_value = cache_mock
        samm_graph = SAMMGraph("graph")
        result = samm_graph.find_by_urn("urn")

        assert result == "graph_node"
        cache_mock.get_by_urn.assert_called_once_with("urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.determine_element_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.find_by_name")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_determine_access_path(self, _, find_by_name_mock, determine_element_access_path_mock):
        find_by_name_mock.side_effect = (["base_element"], [])
        determine_element_access_path_mock.return_value = ["access_path"]
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph.determine_access_path("base_element_name")

        assert result == ["access_path"]
        find_by_name_mock.assert_called_once_with("base_element_name")
        determine_element_access_path_mock.assert_called_once_with("base_element")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._SAMMGraph__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_determine_element_access_path_with_payload_name(
        self,
        _,
        isinstance_mock,
        property_mock,
        determine_access_path_mock,
    ):
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.payload_name = "payload_name"
        determine_access_path_mock.return_value = "element_access_path"
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["payload_name"]])

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._SAMMGraph__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_determine_element_access_path_base_element_name(
        self,
        _,
        isinstance_mock,
        property_mock,
        determine_access_path_mock,
    ):
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.name = "base_element_name"
        base_element_mock.payload_name = None
        determine_access_path_mock.return_value = "element_access_path"
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["base_element_name"]])

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_determine_access_path_base_element_is_none(self, _):
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(None, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_determine_access_path_parent_element_is_none(self, _):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = None
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_determine_access_path_parent_element_is_empty_list(self, _):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = []
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_private_determine_access_path_parent_payload_name(self, _, isinstance_mock):
        parent_element_mock = mock.MagicMock(name="parent_element")
        parent_element_mock.parent_elements = []
        parent_element_mock.payload_name = "payload_name"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = [parent_element_mock]
        isinstance_mock.return_value = True
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_name", "path"]]

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.populate_with_meta_data")
    def test_private_determine_access_path_parent_name(self, _, isinstance_mock):
        parent_element_mock = mock.MagicMock(name="parent_element")
        parent_element_mock.parent_elements = []
        parent_element_mock.payload_name = None
        parent_element_mock.name = "payload_element_name"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = [parent_element_mock]
        isinstance_mock.return_value = True
        samm_graph = SAMMGraph("graph", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_element_name", "path"]]
