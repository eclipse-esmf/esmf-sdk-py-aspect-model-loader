"""Local file resolver test suit."""

from unittest import mock

import pytest

from rdflib import RDF

from esmf_aspect_meta_model_python.resolver.local_file import LocalFileResolver


class TestLocalFileResolver:
    """Local file resolver test suit."""

    def test_init(self):
        result = LocalFileResolver()

        assert result.file_path is None

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.exists")
    def test_validate_file(self, exists_mock):
        exists_mock.return_value = True
        resolver = LocalFileResolver()
        result = resolver.validate_file("file_path")

        assert result is None
        exists_mock.assert_called_once_with("file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.exists")
    def test_validate_file_raise_error(self, exists_mock):
        exists_mock.return_value = False
        resolver = LocalFileResolver()
        with pytest.raises(FileNotFoundError) as error:
            resolver.validate_file("file_path")

        assert str(error.value) == "Could not find a file file_path"
        exists_mock.assert_called_once_with("file_path")

    def test_parse_namespace_no_data(self):
        resolver = LocalFileResolver()
        result = resolver._parse_namespace("urn:samm:org.eclipse.esmf.samm:2.1.0#")

        assert len(result) == 2
        namespace_specific_str, version = result
        assert namespace_specific_str is None
        assert version is None

    def test_parse_namespace(self):
        resolver = LocalFileResolver()
        result = resolver._parse_namespace("urn:samm:com.boschsemanticstack.digitalcv.instance:0.2.0#")

        assert len(result) == 2
        namespace_specific_str, version = result
        assert namespace_specific_str == "com.boschsemanticstack.digitalcv.instance"
        assert version == "0.2.0"

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.join")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._parse_namespace")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.Path")
    def test_get_dirs_for_advanced_loading(self, path_mock, parse_namespace_mock, join_mock):
        path_mock.return_value = path_mock
        path_mock.parents = ["parent_path", "path", "base_path"]
        graph_mock = mock.MagicMock(name="graph")
        graph_mock.namespace_manager.namespaces.return_value = [("prefix", "namespace")]
        parse_namespace_mock.return_value = "namespace", "version"
        join_mock.return_value = "join_path"
        resolver = LocalFileResolver()
        resolver.graph = graph_mock
        result = resolver._get_dirs_for_advanced_loading("file_path")

        assert result == ["join_path"]
        path_mock.assert_called_once_with("file_path")
        graph_mock.namespace_manager.namespaces.assert_called_once()
        parse_namespace_mock.assert_called_once_with("namespace")
        join_mock.assert_called_once_with("base_path", "namespace", "version")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._get_dirs_for_advanced_loading")
    def test_get_dependency_folders(self, get_dirs_for_advanced_loading_mock):
        graph_mock = mock.MagicMock(name="graph")
        get_dirs_for_advanced_loading_mock.return_value = "dependency_folders"
        resolver = LocalFileResolver()
        resolver.file_path = "base_file_path"
        resolver.graph = graph_mock
        result = resolver._get_dependency_folders("file_path")

        assert result == "dependency_folders"
        graph_mock.parse.assert_called_once_with("file_path", format="turtle")
        get_dirs_for_advanced_loading_mock.assert_called_once_with("file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.exists")
    def test_get_additional_files_from_dir_raise_error(self, exists_mock):
        exists_mock.return_value = False
        resolver = LocalFileResolver()
        with pytest.raises(NotADirectoryError) as error:
            resolver._get_additional_files_from_dir("file_path")

        assert str(error.value) == "Directory not found: file_path"
        exists_mock.assert_called_once_with("file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.Path")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.exists")
    def test_get_additional_files_from_dir(self, exists_mock, path_mock):
        exists_mock.return_value = True
        path_mock.return_value = path_mock
        path_mock.glob.return_value = ["additional_file_path"]
        resolver = LocalFileResolver()
        result = resolver._get_additional_files_from_dir("file_path")

        assert result == ["additional_file_path"]
        exists_mock.assert_called_once_with("file_path")
        path_mock.assert_called_once_with("file_path")
        path_mock.glob.assert_called_once_with("*.ttl")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.print")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._get_additional_files_from_dir")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._get_dependency_folders")
    def test_get_dependency_files_raise_error(
        self,
        get_dependency_folders_mock,
        get_additional_files_from_dir_mock,
        print_mock,
    ):
        get_dependency_folders_mock.side_effect = (["dependency_folder"], Exception("error"))
        get_additional_files_from_dir_mock.return_value = ["additional_file_path"]
        resolver = LocalFileResolver()
        file_dependencies = {}
        folder_dependencies = {}
        with pytest.raises(Exception) as error:
            resolver._get_dependency_files(file_dependencies, folder_dependencies, "file_path")

        assert str(error.value) == "error"
        get_dependency_folders_mock.assert_has_calls([mock.call("file_path"), mock.call("additional_file_path")])
        get_additional_files_from_dir_mock.assert_called_once_with("dependency_folder")
        print_mock.assert_called_once_with("Could not parse file additional_file_path\nError: error")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._get_additional_files_from_dir")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._get_dependency_folders")
    def test_get_dependency_files(self, get_dependency_folders_mock, get_additional_files_from_dir_mock):
        get_dependency_folders_mock.return_value = ["dependency_folder"]
        get_additional_files_from_dir_mock.return_value = ["additional_file_path"]
        resolver = LocalFileResolver()
        file_dependencies = {}
        folder_dependencies = {}
        result = resolver._get_dependency_files(file_dependencies, folder_dependencies, "file_path")

        assert result == {"file_path": ["dependency_folder"], "additional_file_path": ["dependency_folder"]}
        get_dependency_folders_mock.assert_has_calls([mock.call("file_path"), mock.call("additional_file_path")])
        get_additional_files_from_dir_mock.assert_called_once_with("dependency_folder")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._get_dependency_files")
    def test_parse_namespaces(self, get_dependency_files_mock):
        resolver = LocalFileResolver()
        result = resolver.parse_namespaces("aspect_file_path")

        assert result is None
        get_dependency_files_mock.assert_called_once_with({}, {}, "aspect_file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver.parse_namespaces")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver._find_aspect_urn")
    def test_read(self, find_aspect_urn_mock, parse_namespaces_mock):
        graph_mock = mock.MagicMock(name="graph")
        resolver = LocalFileResolver()
        resolver.graph = graph_mock
        result = resolver.read("file_path")

        assert result == graph_mock
        assert resolver.file_path == "file_path"
        graph_mock.parse.assert_called_once_with("file_path")
        find_aspect_urn_mock.assert_called_once()
        parse_namespaces_mock.assert_called_once_with("file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.Path")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.SAMM")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver.get_samm_version")
    def test_find_aspect_urn(self, get_samm_version_mock, samm_class_mock, path_mock):
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_urn.return_value = "aspect_urn"
        samm_class_mock.return_value = samm_mock
        samm_class_mock.aspect = "aspect"
        get_samm_version_mock.return_value = "1.2.3"
        graph_mock = mock.MagicMock(mname="graph")
        graph_mock.subjects.return_value = ["path#aspect_name", "path#another_aspect_urn"]
        path_mock.return_value = path_mock
        path_mock.stem = "aspect"
        resolver = LocalFileResolver()
        resolver.file_path = "path/to/file/aspect_name.ttl"
        resolver.graph = graph_mock
        result = resolver._find_aspect_urn()

        assert result is None
        get_samm_version_mock.assert_called_once()
        samm_mock.get_urn.assert_called_once_with("aspect")
        graph_mock.subjects.assert_called_once_with(predicate=RDF.type, object="aspect_urn")
        path_mock.assert_called_once_with("path/to/file/aspect_name.ttl")

    def test_get_aspect_urn(self):
        resolver = LocalFileResolver()
        resolver.aspect_urn = "aspect_urn"
        result = resolver.get_aspect_urn()

        assert result == "aspect_urn"
