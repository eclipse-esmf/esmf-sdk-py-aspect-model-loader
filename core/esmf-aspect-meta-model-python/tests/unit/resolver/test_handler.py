"""Input handler test suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.resolver.handler import InputHandler


class TestInputHandler:
    """Input handler test suit."""

    def test_init(self):
        result = InputHandler("input_data", "input_type")

        assert result.input_data == "input_data"
        assert result.input_type == "input_type"

    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.LocalFileResolver")
    def test_get_reader_local_file(self, local_file_resolver_mock):
        local_file_resolver_mock.return_value = "local_file_reader"
        handler = InputHandler("file_path", InputHandler.FILE_PATH_TYPE)
        result = handler.get_reader()

        assert result == "local_file_reader"
        local_file_resolver_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.DataStringResolver")
    def test_get_reader_data_string(self, data_string_resolver):
        data_string_resolver.return_value = "data_string_reader"
        handler = InputHandler("data", InputHandler.DATA_STRING)
        result = handler.get_reader()

        assert result == "data_string_reader"
        data_string_resolver.assert_called_once()

    def test_get_reader_raise_error(self):
        handler = InputHandler("input_data", "input_type")
        with pytest.raises(ValueError) as error:
            handler.get_reader()

        assert str(error.value) == "Unknown input type"

    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.InputHandler.get_reader")
    def test_get_rdf_graph(self, get_reader_mock):
        reader_mock = mock.MagicMock(name="reader")
        reader_mock.read.return_value = "graph"
        reader_mock.get_aspect_urn.return_value = "aspect_urn"
        get_reader_mock.return_value = reader_mock
        handler = InputHandler("input_data", "input_type")
        result = handler.get_rdf_graph()

        assert len(result) == 2
        graph, aspect_urn = result
        assert graph == "graph"
        assert aspect_urn == "aspect_urn"

    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.os.path.isfile")
    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.InputHandler.contains_newline")
    def test_guess_input_type_file_path(self, contains_newline_mock, isfile_mock):
        contains_newline_mock.return_value = False
        isfile_mock.return_value = True
        handler = InputHandler("input_data", "input_type")
        result = handler.guess_input_type("input_str")

        assert result == InputHandler.FILE_PATH_TYPE
        contains_newline_mock.assert_called_once_with("input_str")
        isfile_mock.assert_called_once_with("input_str")

    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.InputHandler.contains_newline")
    def test_guess_input_type_data_string_with_newline(self, contains_newline_mock):
        contains_newline_mock.return_value = True
        handler = InputHandler("input_data", "input_type")
        result = handler.guess_input_type("input_str")

        assert result == InputHandler.DATA_STRING
        contains_newline_mock.assert_called_once_with("input_str")

    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.os.path.isfile")
    @mock.patch("esmf_aspect_meta_model_python.resolver.handler.InputHandler.contains_newline")
    def test_guess_input_type_data_string_not_file(self, contains_newline_mock, isfile_mock):
        contains_newline_mock.return_value = False
        isfile_mock.return_value = False
        handler = InputHandler("input_data", "input_type")
        result = handler.guess_input_type("input_str")

        assert result == InputHandler.DATA_STRING
        contains_newline_mock.assert_called_once_with("input_str")
        isfile_mock.assert_called_once_with("input_str")

    def test_contains_newline_true(self):
        handler = InputHandler("input_data", "input_type")
        result = handler.contains_newline("input_str\n")

        assert result is True

    def test_contains_newline_false(self):
        handler = InputHandler("input_data", "input_type")
        result = handler.contains_newline("input_str")

        assert result is False
