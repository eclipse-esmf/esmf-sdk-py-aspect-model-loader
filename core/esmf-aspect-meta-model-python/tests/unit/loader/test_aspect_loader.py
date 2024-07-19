"""Aspect model Loader test suite."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.aspect_loader import AspectLoader


class TestAspectLoader:
    """Aspect model Loader test suite."""

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMMGraph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_init(self, default_element_cache_mock, samm_graph_mock):
        default_element_cache_mock.return_value = "cache"
        samm_graph_mock.return_value = "graph"
        result = AspectLoader()

        assert result._cache == "cache"
        assert result._graph == "graph"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMMGraph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_init_with_defaults(self, default_element_cache_mock, samm_graph_mock):
        default_element_cache_mock.return_value = "cache"
        samm_graph_mock.return_value = "graph"
        result = AspectLoader()

        assert result._cache == "cache"
        assert result._graph == "graph"
        default_element_cache_mock.assert_called_once()
        samm_graph_mock.assert_called_once_with()

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMMGraph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_graph(self, default_element_cache_mock, samm_graph_mock):
        default_element_cache_mock.return_value = "cache"
        samm_graph_mock.return_value = "graph"
        loader = AspectLoader()
        result = loader.get_graph()

        assert result == "graph"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMMGraph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_get_samm_version(self, default_element_cache_mock, samm_graph_mock):
        default_element_cache_mock.return_value = "cache"
        graph_mock = mock.MagicMock(name="graph")
        graph_mock.get_samm_version.return_value = "samm_version"
        samm_graph_mock.return_value = graph_mock
        loader = AspectLoader()
        result = loader.get_samm_version()

        assert result == "samm_version"
        graph_mock.get_samm_version.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    def test_prepare_file_path(self, isinstance_mock, path_mock):
        isinstance_mock.return_value = True
        file_path_mock = mock.MagicMock(name="file_path")
        file_path_mock.exists.return_value = True
        path_mock.return_value = file_path_mock
        result = AspectLoader.convert_file_path("file_path")

        assert result == "file_path"
        isinstance_mock.assert_called_once_with("file_path", path_mock)
        path_mock.assert_called_once_with("file_path")
        file_path_mock.exists.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._reset_graph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader.convert_file_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMMGraph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_load_aspect_model(
        self,
        default_element_cache_mock,
        samm_graph_mock,
        convert_file_path_mock,
        reset_graph_mock,
    ):
        default_element_cache_mock.return_value = "cache"
        graph_mock = mock.MagicMock(name="graph")
        graph_mock.parse.return_value = "graph"
        graph_mock.to_python.return_value = "loaded_aspect_model"
        samm_graph_mock.return_value = graph_mock
        convert_file_path_mock.return_value = "converted_file_path"
        loader = AspectLoader()
        result = loader.load_aspect_model("file_path")

        assert result == "loaded_aspect_model"
        convert_file_path_mock.assert_called_once_with("file_path")
        reset_graph_mock.assert_called_once()
        graph_mock.parse.assert_called_once_with("converted_file_path")
        graph_mock.to_python.assert_called_once()
