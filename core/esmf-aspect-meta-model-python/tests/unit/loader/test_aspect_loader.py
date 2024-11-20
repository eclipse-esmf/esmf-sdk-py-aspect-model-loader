"""Aspect model Loader test suite."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.aspect_loader import AspectLoader


class TestAspectLoader:
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMMGraph")
    def test_load_aspect_model(self, samm_graph_mock):
        graph_mock = mock.MagicMock(name="graph")
        graph_mock.to_python.return_value = "python_aspect_nodes"
        samm_graph_mock.return_value = graph_mock
        loader = AspectLoader()
        result = loader.load_aspect_model("graph", "aspect_urn")

        assert result == "python_aspect_nodes"
        samm_graph_mock.assert_called_once_with(graph="graph")
        graph_mock.to_python.assert_called_once_with("aspect_urn")
