"""SAMM Graph test suite."""

from pathlib import Path
from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.samm_graph import SAMMGraph


class TestSAMMGraph:
    """SAMM Graph test suite."""

    def test_init(self):
        result = SAMMGraph("graph", "resolver", "cache")

        assert result._graph == "graph"
        assert result._resolver == "resolver"
        assert result._cache == "cache"
        assert result._samm_version == ""
        assert result._file_path == ""

    def test_get_rdf_graph(self):
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph.get_rdf_graph()

        assert result == "graph"

    def test_get_samm_version(self):
        graph_mock = mock.MagicMock(name="graph")
        namespace_manager_mock = mock.MagicMock(name="namespace_manager")
        namespace_manager_mock.namespaces.return_value = [
            ("prefix", "some_link"),
            ("", "namespace"),
            ("samm", "namespace:path:to:model:3.2.1#"),
        ]
        graph_mock.namespace_manager = namespace_manager_mock
        samm_graph = SAMMGraph(graph_mock, "resolver", "cache")
        result = samm_graph.get_samm_version()

        assert result == "3.2.1"
        namespace_manager_mock.namespaces.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    def test_prepare_file_path(self, isinstance_mock):
        isinstance_mock.return_value = True
        file_path = Path("file_path")
        result = SAMMGraph.convert_file_path(file_path)

        assert result == "file_path"
        isinstance_mock.assert_called_once_with(file_path, Path)

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_samm_version")
    def test_parse(self, get_samm_version_mock):
        graph_mock = mock.MagicMock(name="graph")
        get_samm_version_mock.return_value = "samm_version"
        resolver_mock = mock.MagicMock(name="resolver")
        samm_graph = SAMMGraph(graph_mock, resolver_mock, "cache")
        result = samm_graph.parse("file_path")

        assert result == graph_mock
        assert samm_graph._file_path == "file_path"
        graph_mock.parse.assert_called_once_with("file_path")
        assert samm_graph._samm_version == "samm_version"
        resolver_mock.resolve.assert_called_once_with(graph_mock, "file_path", "samm_version")

    def test_get_model_file_path(self):
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        samm_graph._file_path = "file_path"
        result = samm_graph._get_model_file_path()

        assert result == "file_path"

    def test_get_model_file_path_raise_exception(self):
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        with pytest.raises(ValueError) as error:
            samm_graph._get_model_file_path()

        assert str(error.value) == "Path to the model is empty"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.RDF.type")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMM")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_model_file_path")
    def test_get_nodes_from_graph_with_aspect(self, get_model_file_path_mock, rdf_graph_mock, samm_mock, rdf_type_mock):
        get_model_file_path_mock.return_value = "model_file_path"
        base_graph_mock = mock.MagicMock(name="base_graph")
        base_graph_mock.subjects.return_value = ["aspect_node"]
        rdf_graph_mock.return_value = rdf_graph_mock
        rdf_graph_mock.parse.return_value = base_graph_mock
        samm_mock.return_value = samm_mock
        samm_mock.aspect = "aspect_node_name"
        samm_mock.get_urn.return_value = "aspect_urn"
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        samm_graph._samm_version = "samm_version"
        result = samm_graph.get_nodes_from_graph()

        assert result == ["aspect_node"]
        get_model_file_path_mock.assert_called_once_with("")
        rdf_graph_mock.assert_called_once()
        rdf_graph_mock.parse.assert_called_once_with("model_file_path", format="turtle")
        samm_mock.assert_called_once_with("samm_version")
        samm_mock.get_urn.assert_called_once_with("aspect_node_name")
        base_graph_mock.subjects.assert_called_once_with(predicate=rdf_type_mock, object="aspect_urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.RDF.type")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMM")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_model_file_path")
    def test_get_nodes_from_graph_no_aspect(self, get_model_file_path_mock, rdf_graph_mock, samm_mock, rdf_type_mock):
        get_model_file_path_mock.return_value = "model_file_path"
        base_graph_mock = mock.MagicMock(name="base_graph")
        base_graph_mock.subjects.return_value = []
        base_graph_mock.subject_objects.return_value = [
            ("base_node_name", "<urn:samm:org.eclipse.esmf.samm:2.1.0#nodeName>"),
        ]
        rdf_graph_mock.return_value = rdf_graph_mock
        rdf_graph_mock.parse.return_value = base_graph_mock
        samm_mock.return_value = samm_mock
        samm_mock.aspect = "aspect_node_name"
        samm_mock.get_urn.return_value = "aspect_urn"
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        samm_graph._samm_version = "samm_version"
        result = samm_graph.get_nodes_from_graph()

        assert result == ["base_node_name"]
        base_graph_mock.subject_objects.assert_called_once_with(predicate=rdf_type_mock, unique=True)

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.URIRef")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    def test_get_base_nodes_with_aspect_urn(self, isinstance_mock, uri_ref_mock):
        isinstance_mock.return_value = False
        uri_ref_mock.return_value = "aspect_uri_ref"
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph.get_base_nodes("aspect_urn")

        assert result == ["aspect_uri_ref"]
        isinstance_mock.assert_called_once_with("aspect_urn", uri_ref_mock)
        uri_ref_mock.assert_called_once_with("aspect_urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_nodes_from_graph")
    def test_get_base_nodes_no_aspect_urn(self, get_nodes_from_graph_mock):
        get_nodes_from_graph_mock.return_value = ["base_node"]
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph.get_base_nodes()

        assert result == ["base_node"]
        get_nodes_from_graph_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.ModelElementFactory")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_base_nodes")
    def test_to_python(self, get_base_nodes_mock, model_element_factory_mock):
        get_base_nodes_mock.return_value = "base_nodes"
        model_element_factory_mock.return_value = model_element_factory_mock
        model_element_factory_mock.create_all_graph_elements.return_value = ["aspect_elements"]
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        samm_graph._samm_version = "samm_version"
        result = samm_graph.to_python("aspect_urn")

        assert result == ["aspect_elements"]
        get_base_nodes_mock.assert_called_once_with("aspect_urn")
        model_element_factory_mock.assert_called_once_with("samm_version", "graph", "cache")
        model_element_factory_mock.create_all_graph_elements.assert_called_once_with("base_nodes")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.DefaultElementCache")
    def test_find_by_name(self, default_element_cache_mock):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_name.return_value = "graph_node"
        default_element_cache_mock.return_value = cache_mock
        samm_graph = SAMMGraph("graph", "resolver")
        result = samm_graph.find_by_name("element_name")

        assert result == "graph_node"
        cache_mock.get_by_name.assert_called_once_with("element_name")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.DefaultElementCache")
    def test_find_by_urn(self, default_element_cache_mock):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_urn.return_value = "graph_node"
        default_element_cache_mock.return_value = cache_mock
        samm_graph = SAMMGraph("graph", "resolver")
        result = samm_graph.find_by_urn("urn")

        assert result == "graph_node"
        cache_mock.get_by_urn.assert_called_once_with("urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.determine_element_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.find_by_name")
    def test_determine_access_path(
        self,
        find_by_name_mock,
        determine_element_access_path_mock,
    ):
        find_by_name_mock.side_effect = (["base_element"], [])
        determine_element_access_path_mock.return_value = ["access_path"]
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph.determine_access_path("base_element_name")

        assert result == ["access_path"]
        find_by_name_mock.assert_called_once_with("base_element_name")
        determine_element_access_path_mock.assert_called_once_with("base_element")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._SAMMGraph__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    def test_determine_element_access_path_with_payload_name(
        self,
        isinstance_mock,
        property_mock,
        determine_access_path_mock,
    ):
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.payload_name = "payload_name"
        determine_access_path_mock.return_value = "element_access_path"
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["payload_name"]])

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._SAMMGraph__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    def test_determine_element_access_path_base_element_name(
        self,
        isinstance_mock,
        property_mock,
        determine_access_path_mock,
    ):
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.name = "base_element_name"
        base_element_mock.payload_name = None
        determine_access_path_mock.return_value = "element_access_path"
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["base_element_name"]])

    def test_determine_access_path_base_element_is_none(self):
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(None, "path")

        assert result == "path"

    def test_determine_access_path_parent_element_is_none(self):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = None
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, "path")

        assert result == "path"

    def test_determine_access_path_parent_element_is_empty_list(self):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = []
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    def test_private_determine_access_path_parent_payload_name(self, isinstance_mock):
        parent_element_mock = mock.MagicMock(name="parent_element")
        parent_element_mock.parent_elements = []
        parent_element_mock.payload_name = "payload_name"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = [parent_element_mock]
        isinstance_mock.return_value = True
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_name", "path"]]

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    def test_private_determine_access_path_parent_name(self, isinstance_mock):
        parent_element_mock = mock.MagicMock(name="parent_element")
        parent_element_mock.parent_elements = []
        parent_element_mock.payload_name = None
        parent_element_mock.name = "payload_element_name"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = [parent_element_mock]
        isinstance_mock.return_value = True
        samm_graph = SAMMGraph("graph", "resolver", "cache")
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_element_name", "path"]]
