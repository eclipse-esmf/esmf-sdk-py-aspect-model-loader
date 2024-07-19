"""Aspect Meta Model Resolver test suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.resolver.meta_model import AspectMetaModelResolver


class TestAspectMetaModelResolver:
    """Aspect Meta Model Resolver test suit."""

    def test_init(self):
        result = AspectMetaModelResolver("base_path")

        assert result._base_path == "base_path"

    @mock.patch("esmf_aspect_meta_model_python.resolver.meta_model.Path")
    def test_init_with_defaults(self, path_mock):
        path_mock.return_value = path_mock
        path_mock.parents = ["parent_1", "parent_2", "parent_3", "parent_4"]
        result = AspectMetaModelResolver()

        assert result._base_path == "parent_3"
        path_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.resolver.meta_model.glob")
    @mock.patch("esmf_aspect_meta_model_python.resolver.meta_model.join")
    def test_get_samm_files(self, join_mock, glob_mock):
        join_mock.return_value = "path_template"
        glob_mock.return_value = ["samm_file_1", "samm_file_2"]
        aspect_resolver = AspectMetaModelResolver("base_path")
        aspect_resolver.samm_folder_path = "samm_folder_path"
        result = aspect_resolver.get_samm_files("meta_model_version")

        assert sorted(result) == ["samm_file_1", "samm_file_2"]
        join_mock.assert_called_once_with("base_path", "samm_folder_path", "**", "meta_model_version", "*.ttl")

    @mock.patch("esmf_aspect_meta_model_python.resolver.meta_model.exists")
    def test_validate_file(self, exists_mock):
        exists_mock.return_value = False
        with pytest.raises(FileNotFoundError) as error:
            AspectMetaModelResolver.validate_file("file_path")

        assert str(error.value) == (
            "File file_path not found. \n"
            "Try to install SAMM Meta Model using 'download-samm-release' or 'download-samm-branch' command"
        )
        exists_mock.assert_called_once_with("file_path")

    @mock.patch("esmf_aspect_meta_model_python.resolver.meta_model.AspectMetaModelResolver.validate_file")
    @mock.patch("esmf_aspect_meta_model_python.resolver.meta_model.AspectMetaModelResolver.get_samm_files")
    def test_parse(self, get_samm_files_mock, validate_file_mock):
        get_samm_files_mock.return_value = ["samm_file_path"]
        aspect_graph_mock = mock.MagicMock(name="graph")
        aspect_resolver = AspectMetaModelResolver("base_path")
        result = aspect_resolver.parse(aspect_graph_mock, "meta_model_version")

        assert result is None
        get_samm_files_mock.assert_called_once_with("meta_model_version")
        validate_file_mock.assert_called_once_with("samm_file_path")
        aspect_graph_mock.parse.assert_called_once_with("samm_file_path", format="turtle")
