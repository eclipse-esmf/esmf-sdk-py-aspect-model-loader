"""SAMM Meta Model functions test suite."""

from unittest import mock

import pytest

from rdflib.term import URIRef

from esmf_aspect_meta_model_python.samm_meta_model import SammUnitsGraph


class TestSammCli:
    """SAMM Units Graph tests."""

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_units")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._validate_path")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_file_path")
    def test_init(self, get_file_path_mock, validate_path_mock, get_units_mock):
        get_file_path_mock.return_value = "unit_file_path"
        get_units_mock.return_value = "graph"
        result = SammUnitsGraph()

        assert result.graph == "graph"
        get_file_path_mock.assert_called_once()
        validate_path_mock.assert_called_once()
        get_units_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_units")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._validate_path")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.join")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.Path")
    def test_get_file_path(self, path_mock, join_mock, _, get_units_mock):
        base_path_mock = mock.MagicMock()
        base_path_mock.parents = ["parent", "child"]
        path_mock.return_value = path_mock
        path_mock.resolve.return_value = base_path_mock
        join_mock.return_value = "file_path"
        get_units_mock.return_value = "graph"
        result = SammUnitsGraph()

        assert result.unit_file_path == "file_path"
        path_mock.assert_called_once()
        path_mock.resolve.assert_called_once()
        join_mock.assert_called_once_with("parent", SammUnitsGraph.UNIT_FILE_PATH)

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_units")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.exists")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_file_path")
    def test_validate_path(self, get_file_path_mock, exists_mock, get_units_mock):
        get_file_path_mock.return_value = "unit_file_path"
        exists_mock.return_value = True
        get_units_mock.return_value = "graph"
        result = SammUnitsGraph()

        assert result is not None
        exists_mock.assert_called_once_with("unit_file_path")

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.exists")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_file_path")
    def test_validate_path_with_exception(self, get_file_path_mock, exists_mock):
        get_file_path_mock.return_value = "unit_file_path"
        exists_mock.return_value = False
        with pytest.raises(ValueError) as error:
            SammUnitsGraph()

        assert str(error.value) == "There is no such file unit_file_path"
        exists_mock.assert_called_once_with("unit_file_path")

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.rdflib.Graph")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._validate_path")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_file_path")
    def test_get_units(self, get_file_path_mock, validate_path_mock, rdflib_graph_mock):
        get_file_path_mock.return_value = "unit_file_path"
        graph_mock = mock.MagicMock()
        rdflib_graph_mock.return_value = graph_mock
        result = SammUnitsGraph()

        assert result._graph == graph_mock
        rdflib_graph_mock.assert_called_once()
        graph_mock.parse.assert_called_once_with("unit_file_path", format="turtle")

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_units")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._validate_path")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_file_path")
    def test_get_nested_data_unit(self, get_file_path_mock, _, get_units_mock):
        get_file_path_mock.return_value = "unit_file_path"
        get_units_mock.return_value = "graph"
        units_graph = SammUnitsGraph()
        result = units_graph._get_nested_data("prefix#Unit")

        assert result == ("Unit", "prefix#Unit")

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph.get_info")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_units")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._validate_path")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_file_path")
    def test_get_nested_data_not_unit(self, get_file_path_mock, _, get_units_mock, get_info_mock):
        get_file_path_mock.return_value = "unit_file_path"
        get_units_mock.return_value = "graph"
        get_info_mock.return_value = "nested_value"
        units_graph = SammUnitsGraph()
        result = units_graph._get_nested_data("prefix#unitType")

        assert result == ("unitType", "nested_value")
        get_info_mock.assert_called_once_with("unit:unitType")

    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_nested_data")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_units")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._validate_path")
    @mock.patch("esmf_aspect_meta_model_python.samm_meta_model.SammUnitsGraph._get_file_path")
    def test_get_info(self, get_file_path_mock, _, get_units_mock, isinstance_mock, get_nested_data_mock):
        get_file_path_mock.return_value = "unit_file_path"
        isinstance_mock.side_effect = (False, URIRef, URIRef)
        get_nested_data_mock.side_effect = [("type_key", "type_description"), ("sub_unit", "sub_unit_description")]
        row_1_mock = mock.MagicMock()
        row_1_mock.key = "prefix#unitType"
        row_1_mock.value = "unit_1"
        row_2_mock = mock.MagicMock()
        row_2_mock.key = "prefix#type"
        row_2_mock.value = "unit_2"
        row_3_mock = mock.MagicMock()
        row_3_mock.key = "prefix#otherUnit"
        row_3_mock.value = "unit_3"
        graph_mock = mock.MagicMock()
        graph_mock.query.return_value = [row_1_mock, row_2_mock, row_3_mock]
        get_units_mock.return_value = graph_mock
        units_graph = SammUnitsGraph()
        result = units_graph.get_info("unit:unit_name")

        assert "unitType" in result
        assert result["unitType"] == "unit_1"
        assert "otherUnit" in result
        assert len(result["otherUnit"]) == 1
        assert "sub_unit" in result["otherUnit"][0]
        assert result["otherUnit"][0]["sub_unit"] == "sub_unit_description"
        graph_mock.query.assert_called_once_with("SELECT ?key ?value WHERE {unit:unit_name ?key ?value .}")
        isinstance_mock.assert_has_calls(
            [
                mock.call("unit_1", URIRef),
                mock.call("unit_2", URIRef),
                mock.call("unit_3", URIRef),
            ]
        )
        get_nested_data_mock.assert_has_calls([mock.call("unit_2"), mock.call("unit_3")])
