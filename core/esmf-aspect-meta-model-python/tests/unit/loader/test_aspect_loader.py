"""AspectLoader test suite."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.aspect_loader import AspectLoader


class TestAspectLoader:
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_init(self, default_element_cache_mock):
        default_element_cache_mock.return_value = "cache"
        result = AspectLoader()

        assert result._cache == "cache"
        default_element_cache_mock.assert_called_once()

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._load_aspect_model_from_multiple_files"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_load_aspect_model(self, default_element_cache_mock, load_aspect_model_from_multiple_files_mock):
        default_element_cache_mock.return_value = "cache"
        load_aspect_model_from_multiple_files_mock.return_value = "result"
        loader = AspectLoader()
        result = loader.load_aspect_model("file_path")

        assert result == "result"
        load_aspect_model_from_multiple_files_mock.assert_called_once_with(["file_path"])

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.exists")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_additional_files_from_dir(self, default_element_cache_mock, exists_mock, path_mock):
        default_element_cache_mock.return_value = "cache"
        exists_mock.return_value = True
        path_mock.return_value = path_mock
        path_mock.glob.return_value = ["additional_file_path"]
        loader = AspectLoader()
        result = loader._get_additional_files_from_dir("file_path")

        assert result == ["additional_file_path"]
        exists_mock.assert_called_once_with("file_path")
        path_mock.assert_called_once_with("file_path")
        path_mock.glob.assert_called_once_with("*.ttl")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.exists")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_additional_files_from_dir_raise_exception(self, default_element_cache_mock, exists_mock):
        default_element_cache_mock.return_value = "cache"
        exists_mock.return_value = False
        loader = AspectLoader()
        with pytest.raises(NotADirectoryError) as error:
            loader._get_additional_files_from_dir("file_path")

        assert str(error.value) == "Directory not found: file_path"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_parse_namespace(self, default_element_cache_mock):
        default_element_cache_mock.return_value = "cache"
        loader = AspectLoader()
        result = loader._parse_namespace("urn:samm:some.address:0.1.2#")

        assert result == ("some.address", "0.1.2")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.join")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._parse_namespace")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_dirs_for_advanced_loading(
        self,
        default_element_cache_mock,
        path_mock,
        parse_namespace_mock,
        join_mock,
    ):
        default_element_cache_mock.return_value = "cache"
        path_mock.return_value = path_mock
        path_mock.parents = ["path", "some_path", "base_path"]
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.namespace_manager.namespaces.return_value = [
            ("prefix", "namespace"),
        ]
        parse_namespace_mock.return_value = ("namespace_specific_str", "version")
        join_mock.return_value = "paths_for_advanced_loading"
        loader = AspectLoader()
        result = loader._get_dirs_for_advanced_loading(aspect_graph_mock, "file_path")

        assert result == ["paths_for_advanced_loading"]
        path_mock.assert_called_once_with("file_path")
        aspect_graph_mock.namespace_manager.namespaces.assert_called_once()
        parse_namespace_mock.assert_called_once_with("namespace")
        join_mock.assert_called_once_with("base_path", "namespace_specific_str", "version")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.exists")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_prepare_file_paths(self, default_element_cache_mock, path_mock, exists_mock):
        default_element_cache_mock.return_value = "cache"
        path_mock.return_value = "path_of_the_file"
        exists_mock.return_value = True
        loader = AspectLoader()
        result = loader._prepare_file_paths(["file_path"])

        assert result == ["file_path"]
        path_mock.assert_called_once_with("file_path")
        exists_mock.assert_called_once_with("path_of_the_file")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.exists")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_prepare_file_paths_raise_exception(self, default_element_cache_mock, path_mock, exists_mock):
        default_element_cache_mock.return_value = "cache"
        path_mock.return_value = "path_of_the_file"
        exists_mock.return_value = False
        loader = AspectLoader()
        with pytest.raises(FileNotFoundError) as error:
            loader._prepare_file_paths(["file_path"])

        assert str(error.value) == "Could not find a file file_path"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._get_dirs_for_advanced_loading")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.rdflib")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_dependency_folders(
        self,
        default_element_cache_mock,
        rdflib_mock,
        get_dirs_for_advanced_loading_mock,
    ):
        default_element_cache_mock.return_value = "cache"
        graph_mock = mock.MagicMock(name="graph")
        get_dirs_for_advanced_loading_mock.return_value = "dependency_folders"
        rdflib_mock.Graph.return_value = graph_mock
        loader = AspectLoader()
        result = loader.get_dependency_folders("file_path")

        assert result == "dependency_folders"
        rdflib_mock.Graph.assert_called_once()
        graph_mock.parse.assert_called_once_with("file_path", format="turtle")
        get_dirs_for_advanced_loading_mock.assert_called_once_with(graph_mock, "file_path")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._get_additional_files_from_dir")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader.get_dependency_folders")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_dependency_files(
        self,
        default_element_cache_mock,
        get_dependency_folders_mock,
        get_additional_files_from_dir_mock,
    ):
        default_element_cache_mock.return_value = "cache"
        get_dependency_folders_mock.side_effect = (["folder_1", "folder_2"], ["folder_1", "folder_3"])
        get_additional_files_from_dir_mock.side_effect = (["file_1"], ["file_1", "file_2"], ["file_2"])
        file_dependencies = {}
        folder_dependencies = {}
        loader = AspectLoader()
        result = loader._get_dependency_files(file_dependencies, folder_dependencies, "file_1")

        assert "file_1" in result
        assert sorted(result["file_1"]) == ["folder_1", "folder_2"]
        assert "file_2" in result
        assert sorted(result["file_2"]) == ["folder_1", "folder_3"]
        get_dependency_folders_mock.assert_has_calls(
            [
                mock.call("file_1"),
                mock.call("file_2"),
            ]
        )
        get_additional_files_from_dir_mock.assert_has_calls(
            [
                mock.call("folder_1"),
                mock.call("folder_2"),
                mock.call("folder_3"),
            ]
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._get_dependency_files")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_all_dependencies(self, default_element_cache_mock, get_dependency_files_mock):
        default_element_cache_mock.return_value = "cache"
        get_dependency_files_mock.return_value = {"file_1": ["folder_1", "folder_2"]}
        loader = AspectLoader()
        result = loader._get_all_dependencies(["file_path"])

        assert result == {"file_1": ["folder_1", "folder_2"]}
        get_dependency_files_mock.assert_called_once_with({"file_1": ["folder_1", "folder_2"]}, {}, "file_path")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._get_all_dependencies")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._prepare_file_paths")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.rdflib")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_graph(
        self,
        default_element_cache_mock,
        rdflib_mock,
        prepare_file_paths_mock,
        get_all_dependencies_mock,
    ):
        default_element_cache_mock.return_value = "cache"
        graph_mock = mock.MagicMock(name="graph")
        rdflib_mock.Graph.return_value = graph_mock
        prepare_file_paths_mock.return_value = ["prepared_file_path"]
        get_all_dependencies_mock.return_value = ["prepared_file_path", "dependency_file"]
        loader = AspectLoader()
        result = loader._get_graph(["file_path"])

        assert result == graph_mock
        rdflib_mock.Graph.assert_called_once()
        prepare_file_paths_mock.assert_called_once_with(["file_path"])
        get_all_dependencies_mock.assert_called_once_with(["prepared_file_path"])
        graph_mock.parse.assert_has_calls(
            [
                mock.call("prepared_file_path", format="turtle"),
                mock.call("dependency_file", format="turtle"),
            ]
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.ModelElementFactory")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectMetaModelResolver.resolve_meta_model")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.rdflib.URIRef")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.rdflib.RDF")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMM")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._AspectLoader__extract_samm_version")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._get_graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_load_aspect_model_from_multiple_files(
        self,
        default_element_cache_mock,
        get_graph_mock,
        extract_samm_version_mock,
        samm_mock,
        rdf_mock,
        uri_ref_mock,
        resolve_meta_model_mock,
        model_element_factory_mock,
    ):
        cache_mock = mock.MagicMock(name="cache")
        default_element_cache_mock.return_value = cache_mock
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "aspect_urn"
        get_graph_mock.return_value = aspect_graph_mock
        extract_samm_version_mock.return_value = "meta_model_version"
        samm_instance_mock = mock.MagicMock(name="SAMM")
        samm_instance_mock.get_urn.return_value = "object"
        samm_mock.return_value = samm_instance_mock
        samm_mock.aspect = "SAMM_aspect"
        rdf_mock.type = "rdf_type"
        uri_ref_mock.__contains__.return_value = False
        uri_ref_mock.return_value = "aspect_urn"
        model_element_factory_mock.return_value = model_element_factory_mock
        model_element_factory_mock.create_element.return_value = "aspect_element"
        loader = AspectLoader()
        result = loader._load_aspect_model_from_multiple_files(["file_path"])

        assert result == "aspect_element"
        cache_mock.reset.assert_called_once()
        get_graph_mock.assert_called_once_with(["file_path"])
        extract_samm_version_mock.assert_called_once_with(aspect_graph_mock)
        samm_mock.assert_called_once_with("meta_model_version")
        samm_instance_mock.get_urn.assert_called_once_with("SAMM_aspect")
        aspect_graph_mock.value.assert_called_once_with(predicate="rdf_type", object="object")
        uri_ref_mock.assert_called_once_with("aspect_urn")
        resolve_meta_model_mock.assert_called_once_with(aspect_graph_mock, "meta_model_version")
        model_element_factory_mock.assert_called_once_with("meta_model_version", aspect_graph_mock, cache_mock)
        model_element_factory_mock.create_element.assert_called_once_with("aspect_urn")

    def test_extract_samm_version(self):
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.namespace_manager.namespaces.return_value = [("samm", "namespace:version#")]
        result = AspectLoader._AspectLoader__extract_samm_version(aspect_graph_mock)

        assert result == "version"
        aspect_graph_mock.namespace_manager.namespaces.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_find_by_name(self, default_element_cache_mock):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_name.return_value = "graph_node"
        default_element_cache_mock.return_value = cache_mock
        loader = AspectLoader()
        result = loader.find_by_name("element_name")

        assert result == "graph_node"
        cache_mock.get_by_name.assert_called_once_with("element_name")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_find_by_urn(self, default_element_cache_mock):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_urn.return_value = "graph_node"
        default_element_cache_mock.return_value = cache_mock
        loader = AspectLoader()
        result = loader.find_by_urn("urn")

        assert result == "graph_node"
        cache_mock.get_by_urn.assert_called_once_with("urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader.determine_element_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader.find_by_name")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_determine_access_path(
        self,
        default_element_cache_mock,
        find_by_name_mock,
        determine_element_access_path_mock,
    ):
        default_element_cache_mock.return_value = "cache"
        find_by_name_mock.side_effect = (["base_element"], [])
        determine_element_access_path_mock.return_value = ["access_path"]
        loader = AspectLoader()
        result = loader.determine_access_path("base_element_name")

        assert result == ["access_path"]
        find_by_name_mock.assert_called_once_with("base_element_name")
        determine_element_access_path_mock.assert_called_once_with("base_element")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._AspectLoader__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_determine_element_access_path_with_payload_name(
        self, default_element_cache_mock, isinstance_mock, property_mock, determine_access_path_mock
    ):
        default_element_cache_mock.return_value = "cache"
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.payload_name = "payload_name"
        determine_access_path_mock.return_value = "element_access_path"
        loader = AspectLoader()
        result = loader.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["payload_name"]])

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._AspectLoader__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_determine_element_access_path_base_element_name(
        self, default_element_cache_mock, isinstance_mock, property_mock, determine_access_path_mock
    ):
        default_element_cache_mock.return_value = "cache"
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.name = "base_element_name"
        base_element_mock.payload_name = None
        determine_access_path_mock.return_value = "element_access_path"
        loader = AspectLoader()
        result = loader.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["base_element_name"]])

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_determine_access_path_base_element_is_none(self, default_element_cache_mock):
        default_element_cache_mock.return_value = "cache"
        loader = AspectLoader()
        result = loader._AspectLoader__determine_access_path(None, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_determine_access_path_parent_element_is_none(self, default_element_cache_mock):
        default_element_cache_mock.return_value = "cache"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = None
        loader = AspectLoader()
        result = loader._AspectLoader__determine_access_path(base_element_mock, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_determine_access_path_parent_element_is_empty_list(self, default_element_cache_mock):
        default_element_cache_mock.return_value = "cache"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = []
        loader = AspectLoader()
        result = loader._AspectLoader__determine_access_path(base_element_mock, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_private_determine_access_path_parent_payload_name(self, default_element_cache_mock, isinstance_mock):
        default_element_cache_mock.return_value = "cache"
        parent_element_mock = mock.MagicMock(name="parent_element")
        parent_element_mock.parent_elements = []
        parent_element_mock.payload_name = "payload_name"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = [parent_element_mock]
        isinstance_mock.return_value = True
        loader = AspectLoader()
        result = loader._AspectLoader__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_name", "path"]]
