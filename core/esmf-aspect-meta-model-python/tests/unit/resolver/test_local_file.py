"""Local file resolver test suit."""

from unittest import mock

import pytest

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

    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.Graph")
    @mock.patch("esmf_aspect_meta_model_python.resolver.local_file.LocalFileResolver.validate_file")
    def test_read(self, validate_file_mock, graph_mock):
        rdf_graph_mock = mock.MagicMock(name="rdf_graph")
        graph_mock.return_value = rdf_graph_mock
        resolver = LocalFileResolver()
        result = resolver.read("file_path")

        assert result == rdf_graph_mock
        validate_file_mock.assert_called_once_with("file_path")
        rdf_graph_mock.parse.assert_called_once_with("file_path")

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
    def test_prepare_aspect_model(self, get_dependency_files_mock):
        graph_mock = mock.MagicMock(name="graph")
        resolver = LocalFileResolver()
        resolver.file_path = "aspect_file_path"
        result = resolver.prepare_aspect_model(graph_mock)

        assert result is None
        get_dependency_files_mock.assert_called_once_with({}, {}, "aspect_file_path")
