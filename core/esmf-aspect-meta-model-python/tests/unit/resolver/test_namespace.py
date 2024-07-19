"""Aspect namespace resolver test suite."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.resolver.namespace import AspectNamespaceResolver


class TestAspectNamespaceResolver:
    """Aspect namespace resolver test suite."""

    def test_init(self):
        result = AspectNamespaceResolver()

        assert result.aspect_graph is None

    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.exists")
    def test_validate_file(self, exists_mock):
        exists_mock.return_value = False
        with pytest.raises(FileNotFoundError) as error:
            AspectNamespaceResolver.validate_file("file_path")

        assert str(error.value) == "Could not find a file file_path"

    def test_parse_namespace(self):
        result = AspectNamespaceResolver._parse_namespace("urn:samm:some.address:0.1.2#")

        assert result == ("some.address", "0.1.2")

    def test_parse_namespace_not_valid_samm(self):
        result = AspectNamespaceResolver._parse_namespace("urn:samm:org.eclipse.esmf.samm:not.valid.reference#")

        assert result == (None, None)

    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.join")
    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.AspectNamespaceResolver._parse_namespace")
    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.Path")
    def test_get_dirs_for_advanced_loading(
        self,
        path_mock,
        parse_namespace_mock,
        join_mock,
    ):
        path_mock.return_value = path_mock
        path_mock.parents = ["path", "some_path", "base_path"]
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.namespace_manager.namespaces.return_value = [
            ("prefix", "namespace"),
        ]
        parse_namespace_mock.return_value = ("namespace_specific_str", "version")
        join_mock.return_value = "paths_for_advanced_loading"
        resolver = AspectNamespaceResolver()
        resolver.aspect_graph = aspect_graph_mock
        result = resolver._get_dirs_for_advanced_loading("file_path")

        assert result == ["paths_for_advanced_loading"]
        path_mock.assert_called_once_with("file_path")
        aspect_graph_mock.namespace_manager.namespaces.assert_called_once()
        parse_namespace_mock.assert_called_once_with("namespace")
        join_mock.assert_called_once_with("base_path", "namespace_specific_str", "version")

    @mock.patch(
        "esmf_aspect_meta_model_python.resolver.namespace.AspectNamespaceResolver._get_dirs_for_advanced_loading"
    )
    def test_get_dependency_folders(self, get_dirs_for_advanced_loading_mock):
        get_dirs_for_advanced_loading_mock.return_value = "dependency_folders"
        resolver = AspectNamespaceResolver()
        graph_mock = mock.MagicMock(name="graph")
        resolver.aspect_graph = graph_mock
        result = resolver._get_dependency_folders("file_path")

        assert result == "dependency_folders"
        graph_mock.parse.assert_called_once_with("file_path", format="turtle")
        get_dirs_for_advanced_loading_mock.assert_called_once_with("file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.Path")
    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.exists")
    def test_get_additional_files_from_dir(self, exists_mock, path_mock):
        exists_mock.return_value = True
        path_mock.return_value = path_mock
        path_mock.glob.return_value = ["additional_file_path"]
        resolver = AspectNamespaceResolver()
        result = resolver._get_additional_files_from_dir("file_path")

        assert result == ["additional_file_path"]
        exists_mock.assert_called_once_with("file_path")
        path_mock.assert_called_once_with("file_path")
        path_mock.glob.assert_called_once_with("*.ttl")

    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.exists")
    def test_get_additional_files_from_dir_raise_exception(self, exists_mock):
        exists_mock.return_value = False
        resolver = AspectNamespaceResolver()
        with pytest.raises(NotADirectoryError) as error:
            resolver._get_additional_files_from_dir("file_path")

        assert str(error.value) == "Directory not found: file_path"

    @mock.patch(
        "esmf_aspect_meta_model_python.resolver.namespace.AspectNamespaceResolver._get_additional_files_from_dir"
    )
    @mock.patch("esmf_aspect_meta_model_python.resolver.namespace.AspectNamespaceResolver._get_dependency_folders")
    def test_get_dependency_files(self, get_dependency_folders_mock, get_additional_files_from_dir_mock):
        get_dependency_folders_mock.side_effect = (["folder_1", "folder_2"], ["folder_1", "folder_3"])
        get_additional_files_from_dir_mock.side_effect = (["file_1"], ["file_1", "file_2"], ["file_2"])
        file_dependencies = {}
        folder_dependencies = {}
        resolver = AspectNamespaceResolver()
        result = resolver._get_dependency_files(file_dependencies, folder_dependencies, "file_1")

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

    def test_parse(self):
        pass
