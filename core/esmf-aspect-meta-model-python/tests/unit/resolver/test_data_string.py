"""Data string resolver test suit."""

from unittest import mock

from esmf_aspect_meta_model_python.resolver.data_string import DataStringResolver


class TestDataStringResolver:
    """Data string resolver test suit."""

    @mock.patch("esmf_aspect_meta_model_python.resolver.data_string.Graph")
    def test_read(self, rdf_graph_mock):
        graph_mock = mock.MagicMock(name="graph")
        rdf_graph_mock.return_value = graph_mock
        resolver = DataStringResolver()
        result = resolver.read("data_string")

        assert result == graph_mock
        graph_mock.parse.assert_called_once_with(data="data_string")
