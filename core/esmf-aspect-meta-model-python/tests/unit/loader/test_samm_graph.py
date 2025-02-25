"""SAMM Graph test suite."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.samm_graph import SAMMGraph


class TestSAMMGraph:
    """SAMM Graph test suite."""

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.DefaultElementCache")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Graph")
    def test_init(self, graph_mock, default_element_cache_mock):
        graph_mock.side_effect = ("rdf_graph", "samm_graph")
        default_element_cache_mock.return_value = "cache"
        result = SAMMGraph()

        assert result.rdf_graph == "rdf_graph"
        assert result.samm_graph == "samm_graph"
        assert result._cache == "cache"
        assert result.samm_version is None
        assert result.aspect is None
        assert result.model_elements is None
        assert result._samm is None
        assert result._reader is None

    def test_str(self):
        samm_graph = SAMMGraph()
        samm_graph.samm_version = "1.2.3"
        result = str(samm_graph)

        assert result == "SAMMGraph v1.2.3"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.id")
    def test_repr(self, id_mock):
        id_mock.return_value = "instance_id"
        samm_graph = SAMMGraph()
        result = repr(samm_graph)

        assert result == (
            "<SAMMGraph identifier=instance_id (<class 'esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph'>)>"
        )
        id_mock.assert_called_once_with(samm_graph)

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.InputHandler")
    def test_get_rdf_graph(self, input_handler_mock):
        input_data = "test_data"
        input_type = "data_type"
        reader_mock = mock.MagicMock(name="reade")
        input_handler_mock.return_value.get_reader.return_value = reader_mock
        reader_mock.read.return_value = "rdf_graph"
        samm_graph = SAMMGraph()
        samm_graph._get_rdf_graph(input_data, input_type)

        assert samm_graph.rdf_graph == "rdf_graph"
        input_handler_mock.assert_called_once_with(input_data, input_type)
        input_handler_mock.return_value.get_reader.assert_called_once()
        reader_mock.read.assert_called_once_with(input_data)

    def test_get_samm_version_from_rdf_graph(self):
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.namespace_manager.namespaces.return_value = [
            ("samm", "urn:samm:org.eclipse.esmf.samm:meta-model:2.1.0#"),
        ]
        samm_graph = SAMMGraph()
        samm_graph.rdf_graph = graph_mock
        result = samm_graph._get_samm_version_from_rdf_graph()

        assert result == "2.1.0"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_samm_version_from_rdf_graph")
    def test_get_samm_version(self, get_samm_version_from_rdf_graph_mock):
        get_samm_version_from_rdf_graph_mock.return_value = "1.2.3"
        samm_graph = SAMMGraph()
        samm_graph._get_samm_version()

        assert samm_graph.samm_version == "1.2.3"
        get_samm_version_from_rdf_graph_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_samm_version_from_rdf_graph")
    def test_get_samm_version_raises_value_error(self, get_samm_version_from_rdf_graph_mock):
        get_samm_version_from_rdf_graph_mock.return_value = ""
        samm_graph = SAMMGraph()
        samm_graph.rdf_graph = "rdf_graph"

        with pytest.raises(ValueError) as error:
            samm_graph._get_samm_version()

        assert str(error.value) == (
            "SAMM version number was not found in graph. Could not process RDF graph rdf_graph."
        )
        get_samm_version_from_rdf_graph_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMM")
    def test_get_samm(self, samm_mock):
        samm_mock.return_value = "samm"
        samm_graph = SAMMGraph()
        samm_graph.samm_version = "1.2.3"
        samm_graph._get_samm()

        assert samm_graph._samm == "samm"
        samm_mock.assert_called_once_with("1.2.3")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.AspectMetaModelResolver")
    def test_get_samm_graph(self, aspect_meta_model_resolver_mock):
        samm_graph = SAMMGraph()
        samm_graph.samm_graph = "samm_graph"
        samm_graph.samm_version = "1.2.3"
        result = samm_graph._get_samm_graph()

        assert result is None
        aspect_meta_model_resolver_mock.return_value.parse.assert_called_once_with("samm_graph", "1.2.3")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_samm_graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_samm")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_samm_version")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_rdf_graph")
    def test_parse(self, get_rdf_graph_mock, get_samm_version_mock, get_samm_mock, get_samm_graph_mock):
        samm_graph = SAMMGraph()
        result = samm_graph.parse("input_data", "input_type")

        assert result == samm_graph
        get_rdf_graph_mock.assert_called_once_with("input_data", "input_type")
        get_samm_version_mock.assert_called_once()
        get_samm_mock.assert_called_once()
        get_samm_graph_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.RDF.type")
    def test_get_aspect_urn(self, rdf_type_mock):
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.subjects.return_value = ["aspect_urn", "aspect_urn_2"]
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_urn.return_value = "aspect_type_urn"
        samm_mock.Aspect = "Aspect"
        samm_graph = SAMMGraph()
        samm_graph.rdf_graph = graph_mock
        samm_graph._samm = samm_mock
        result = samm_graph.get_aspect_urn()

        assert result == "aspect_urn"
        graph_mock.subjects.assert_called_once_with(predicate=rdf_type_mock, object="aspect_type_urn")
        samm_mock.get_urn.assert_called_once_with("Aspect")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.RDF.type")
    def test_get_aspect_urn_raise_error(self, rdf_type_mock):
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.subjects.return_value = []
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_urn.return_value = "aspect_type_urn"
        samm_mock.Aspect = "Aspect"
        samm_graph = SAMMGraph()
        samm_graph.rdf_graph = graph_mock
        samm_graph._samm = samm_mock
        with pytest.raises(ValueError) as error:
            samm_graph.get_aspect_urn()

        assert str(error.value) == "Could not found Aspect node in the RDF graph."
        graph_mock.subjects.assert_called_once_with(predicate=rdf_type_mock, object="aspect_type_urn")
        samm_mock.get_urn.assert_called_once_with("Aspect")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.RDF.type")
    def test_get_node_from_graph(self, rdf_type_mock):
        graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.subjects.return_value = ["node1", "node2"]
        samm_graph = SAMMGraph()
        samm_graph.rdf_graph = graph_mock
        node_mock = mock.MagicMock(name="node")
        result = samm_graph._get_node_from_graph(node_mock)

        assert result == ["node1", "node2"]
        graph_mock.subjects.assert_called_once_with(predicate=rdf_type_mock, object=node_mock)

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._get_node_from_graph")
    def test_get_all_model_elements(self, get_node_from_graph_mock):
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.meta_model_elements = ["element1", "element2"]
        samm_mock.get_urn.side_effect = ("urn1", "urn2")
        get_node_from_graph_mock.side_effect = (["node1"], ["node2"])
        samm_graph = SAMMGraph()
        samm_graph._samm = samm_mock
        result = samm_graph.get_all_model_elements()

        assert result == ["node1", "node2"]
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call("element1"),
                mock.call("element2"),
            ]
        )
        get_node_from_graph_mock.assert_has_calls(
            [
                mock.call("urn1"),
                mock.call("urn2"),
            ]
        )

    def test_get_all_model_elements_raises_value_error(self):
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.meta_model_elements = []
        samm_graph = SAMMGraph()
        samm_graph._samm = samm_mock

        with pytest.raises(ValueError) as error:
            samm_graph.get_all_model_elements()

        assert str(error.value) == "There are no SAMM elements in the RDF graph."

    def test_load_aspect_model(self):
        samm_graph = SAMMGraph()
        samm_graph.aspect = "aspect"
        result = samm_graph.load_aspect_model()

        assert result == "aspect"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.ModelElementFactory")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_aspect_urn")
    def test_load_aspect_model_create_element(self, get_aspect_urn_mock, model_element_factory_mock):
        reader_mock = mock.MagicMock(name="reader")
        cache_mock = mock.MagicMock(name="cache")
        samm_graph = SAMMGraph()
        samm_graph.rdf_graph = "rdf_graph"
        samm_graph.samm_graph = "_samm_graph"
        samm_graph._reader = reader_mock
        samm_graph.samm_version = "1.2.3"
        samm_graph._cache = cache_mock
        samm_graph.aspect = None
        get_aspect_urn_mock.return_value = "aspect_urn"
        model_element_factory_mock.return_value = model_element_factory_mock
        model_element_factory_mock.create_element.return_value = "aspect"
        result = samm_graph.load_aspect_model()

        assert result == "aspect"
        get_aspect_urn_mock.assert_called_once()
        reader_mock.prepare_aspect_model.assert_called_once_with("rdf_graph_samm_graph")
        model_element_factory_mock.assert_called_once_with("1.2.3", "rdf_graph_samm_graph", cache_mock)
        model_element_factory_mock.create_element.assert_called_once_with("aspect_urn")

    def test_load_model_elements(self):
        samm_graph = SAMMGraph()
        samm_graph.model_elements = "model_elements"
        result = samm_graph.load_model_elements()

        assert result == "model_elements"

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.ModelElementFactory")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.get_all_model_elements")
    def test_load_model_elements_create_elements(self, get_all_model_elements_mock, model_element_factory_mock):
        reader_mock = mock.MagicMock(name="reader")
        cache_mock = mock.MagicMock(name="cache")
        samm_graph = SAMMGraph()
        samm_graph.rdf_graph = "rdf_graph"
        samm_graph.samm_graph = "_samm_graph"
        samm_graph._reader = reader_mock
        samm_graph.samm_version = "1.2.3"
        samm_graph._cache = cache_mock
        samm_graph.model_elements = None
        get_all_model_elements_mock.return_value = "model_elements"
        model_element_factory_mock.return_value = model_element_factory_mock
        model_element_factory_mock.create_all_graph_elements.return_value = "model_elements"
        result = samm_graph.load_model_elements()

        assert result == "model_elements"
        get_all_model_elements_mock.assert_called_once()
        reader_mock.prepare_aspect_model.assert_called_once_with("rdf_graph_samm_graph")
        model_element_factory_mock.assert_called_once_with("1.2.3", "rdf_graph_samm_graph", cache_mock)
        model_element_factory_mock.create_all_graph_elements.assert_called_once_with("model_elements")

    def test_find_by_name(self):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_name.return_value = "node"
        samm_graph = SAMMGraph()
        samm_graph._cache = cache_mock
        result = samm_graph.find_by_name("element_name")

        assert result == "node"
        cache_mock.get_by_name.assert_called_once_with("element_name")

    def test_find_by_urn(self):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_urn.return_value = "node"
        samm_graph = SAMMGraph()
        samm_graph._cache = cache_mock
        result = samm_graph.find_by_urn("urn")

        assert result == "node"
        cache_mock.get_by_urn.assert_called_once_with("urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.determine_element_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph.find_by_name")
    def test_determine_access_path(self, find_by_name_mock, determine_element_access_path_mock):
        find_by_name_mock.side_effect = (["base_element"], [])
        determine_element_access_path_mock.return_value = ["access_path"]
        samm_graph = SAMMGraph()
        result = samm_graph.determine_access_path("base_element_name")

        assert result == ["access_path"]
        find_by_name_mock.assert_called_once_with("base_element_name")
        determine_element_access_path_mock.assert_called_once_with("base_element")

    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph._SAMMGraph__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.samm_graph.isinstance")
    def test_determine_element_access_path_no_property(
        self,
        isinstance_mock,
        property_mock,
        determine_access_path_mock,
    ):
        isinstance_mock.return_value = False
        base_element_mock = mock.MagicMock(name="base_element")
        determine_access_path_mock.return_value = "element_access_path"
        samm_graph = SAMMGraph()
        result = samm_graph.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [])

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
        samm_graph = SAMMGraph()
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
        samm_graph = SAMMGraph()
        result = samm_graph.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["base_element_name"]])

    def test_determine_access_path_base_element_is_none(self):
        samm_graph = SAMMGraph()
        result = samm_graph._SAMMGraph__determine_access_path(None, "path")

        assert result == "path"

    def test_determine_access_path_parent_element_is_none(self):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = None
        samm_graph = SAMMGraph()
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, "path")

        assert result == "path"

    def test_determine_access_path_parent_element_is_empty_list(self):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = []
        samm_graph = SAMMGraph()
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
        samm_graph = SAMMGraph()
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
        samm_graph = SAMMGraph()
        result = samm_graph._SAMMGraph__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_element_name", "path"]]
