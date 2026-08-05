#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

import pathlib
import subprocess

from unittest import mock

import pytest

from rdflib import Graph

from esmf_aspect_meta_model_python.adaptive_graph import AdaptiveGraph
from esmf_aspect_meta_model_python.constants import SAMM_VERSION


@pytest.fixture
def graph():
    return AdaptiveGraph(samm_version="1.0.0")


class TestAdaptiveGraph:
    """Tests for AdaptiveGraph."""

    def test__initialization_sets_samm_version(self):
        """Verifies the SAMM version is set correctly during initialization."""
        graph = AdaptiveGraph(samm_version="2.0.0")

        assert graph._samm_version == "2.0.0"

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.SammCli")
    def test_get_samm_cli(self, samm_cli_mock):
        """Verifies _get_samm_cli returns a SammCli instance and caches it."""

        class SammCliMock:
            pass

        samm_cli_mock.return_value = SammCliMock()
        cli1 = AdaptiveGraph._get_samm_cli()
        cli2 = AdaptiveGraph._get_samm_cli()

        assert isinstance(cli1, AdaptiveGraph._samm_cli.__class__)
        assert cli1 is cli2  # Should return the same instance

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._get_samm_cli")
    def test_upgrade_ttl_file_returns_content(self, get_samm_cli_mock):
        """Verifies prettyprint is called with the correct path and capture=True."""
        samm_cli_mock = mock.MagicMock(name="samm_cli")
        samm_cli_mock.prettyprint.return_value = "content"
        get_samm_cli_mock.return_value = samm_cli_mock
        graph = AdaptiveGraph(samm_version="1.0.0")
        result = graph._upgrade_ttl_file(pathlib.Path("file.ttl"))

        assert result == "content"
        get_samm_cli_mock.assert_called_once()
        samm_cli_mock.prettyprint.assert_called_once_with("file.ttl", capture=True)

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._get_samm_cli")
    def test_upgrade_ttl_file_raises_runtime_error_on_cli_failure(self, get_samm_cli_mock):
        """Verifies RuntimeError wraps stdout/stderr from a failing CLI call."""
        err = subprocess.CalledProcessError(returncode=1, cmd="prettyprint", output="STDOUT", stderr="STDERR")
        get_samm_cli_mock.side_effect = err
        graph = AdaptiveGraph(samm_version="1.0.0")
        with pytest.raises(RuntimeError) as error:
            graph._upgrade_ttl_file(pathlib.Path("file.ttl"))

        assert str(error.value) == "SAMM CLI failed for file.ttl:\nSTDOUT\nSTDERR"
        get_samm_cli_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._upgrade_ttl_file")
    def test_upgrade_source_returns_upgraded_ttl_file(self, upgrade_ttl_file_mock):
        """Verifies _upgrade_source logs a mismatch warning and delegates to _upgrade_ttl_file."""
        upgrade_ttl_file_mock.return_value = "upgraded content"
        graph = AdaptiveGraph(samm_version="1.0.0")
        result = graph._upgrade_source("source_path")

        assert result == "upgraded content"
        upgrade_ttl_file_mock.assert_called_once_with("source_path")

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._upgrade_ttl_file")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.pathlib.Path")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.tempfile.NamedTemporaryFile")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.print")
    def test_upgrade_data_returns_upgraded_ttl_file_encoded_to_utf8(
        self,
        print_mock,
        named_temporary_file_mock,
        path_mock,
        isinstance_mock,
        upgrade_ttl_file_mock,
    ):
        """Verifies _upgrade_data writes input to a temp file, upgrades it, and deletes the temp file."""
        data_mock = mock.MagicMock(name="data")
        data_mock.encode.return_value = "encoded_data"
        tmp_file_mock = mock.MagicMock(name="tmp_file")
        tmp_file_mock.__enter__.return_value = tmp_file_mock
        tmp_file_mock.name = "tmp_file_name"
        named_temporary_file_mock.return_value = tmp_file_mock
        tmp_path_mock = mock.MagicMock(name="tmp_path")
        path_mock.return_value = tmp_path_mock
        isinstance_mock.return_value = True
        upgrade_ttl_file_mock.return_value = "upgraded content"
        graph = AdaptiveGraph(samm_version="1.0.0")
        result = graph._upgrade_data(data_mock)

        assert result == "upgraded content"
        named_temporary_file_mock.assert_called_once_with("wb", suffix=".ttl", delete=False)
        tmp_file_mock.write.assert_called_once_with("encoded_data")
        path_mock.assert_called_once_with("tmp_file_name")
        upgrade_ttl_file_mock.assert_called_once_with(tmp_path_mock)
        tmp_path_mock.unlink.assert_called_once_with(missing_ok=True)
        print_mock.assert_called_once_with(
            "[INFO] SAMM version mismatch detected in provided data (target v1.0.0) Upgrading..."
        )

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._upgrade_ttl_file")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.pathlib.Path")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.tempfile.NamedTemporaryFile")
    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.print")
    def test_upgrade_data_returns_upgraded_ttl_file(
        self,
        print_mock,
        named_temporary_file_mock,
        path_mock,
        isinstance_mock,
        upgrade_ttl_file_mock,
    ):
        """Verifies _upgrade_data writes input to a temp file, upgrades it, and deletes the temp file."""
        tmp_file_mock = mock.MagicMock(name="tmp_file")
        tmp_file_mock.__enter__.return_value = tmp_file_mock
        tmp_file_mock.name = "tmp_file_name"
        named_temporary_file_mock.return_value = tmp_file_mock
        tmp_path_mock = mock.MagicMock(name="tmp_path")
        path_mock.return_value = tmp_path_mock
        isinstance_mock.return_value = False
        upgrade_ttl_file_mock.return_value = "upgraded content"
        graph = AdaptiveGraph(samm_version="1.0.0")
        result = graph._upgrade_data("original data")

        assert result == "upgraded content"
        named_temporary_file_mock.assert_called_once_with("wb", suffix=".ttl", delete=False)
        tmp_file_mock.write.assert_called_once_with("original data")
        path_mock.assert_called_once_with("tmp_file_name")
        upgrade_ttl_file_mock.assert_called_once_with(tmp_path_mock)
        tmp_path_mock.unlink.assert_called_once_with(missing_ok=True)
        print_mock.assert_called_once_with(
            "[INFO] SAMM version mismatch detected in provided data (target v1.0.0) Upgrading..."
        )

    def test_set_samm_version(self):
        """Verifies set_samm_version updates the internal SAMM version string."""
        graph = AdaptiveGraph(samm_version="1.0.0")
        graph.set_samm_version("2.0.0")

        assert graph._samm_version == "2.0.0"


class TestParse:
    """Tests for AdaptiveGraph.parse."""

    @pytest.mark.parametrize(
        "source,data",
        [
            (None, None),  # Neither provided
            (pathlib.Path("file.ttl"), "data_content"),  # Both provided
        ],
    )
    def test_error_invalid_args(self, graph, source, data):
        """Verifies ValueError is raised when neither or both source and data are provided."""
        with pytest.raises(ValueError, match="Either 'source' or 'data' must be provided."):
            graph.parse(source=source, data=data)

    def test_default_samm_version(self):
        """Verifies the default SAMM version matches the global SAMM_VERSION constant."""
        assert AdaptiveGraph()._samm_version == SAMM_VERSION

    @pytest.mark.parametrize("source_type", [str, pathlib.Path])
    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=False)
    @mock.patch("rdflib.Graph.parse")
    def test_version_match(self, mock_parse, mock_version_check, graph, source_type):
        """Verifies rdflib.Graph.parse is called without upgrading when versions match."""
        source = source_type("file.ttl")
        result = graph.parse(source=source)

        assert result is graph
        mock_version_check.assert_called_once_with(pathlib.Path("file.ttl"), samm_version="1.0.0")
        mock_parse.assert_called_once_with(source=pathlib.Path("file.ttl"), data=None)

    @mock.patch("pathlib.Path")
    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=False)
    @mock.patch("rdflib.Graph.parse")
    def test_version_match_source_str(self, mock_parse, mock_version_check, mock_path):
        """Verifies a string source is coerced to pathlib.Path before version checking and parsing."""
        graph = AdaptiveGraph(samm_version="1.0.0")
        source = "file.ttl"
        result = graph.parse(source=source)

        assert result is graph
        mock_path.assert_called_once_with("file.ttl")
        mock_version_check.assert_called_once_with(mock_path.return_value, samm_version="1.0.0")
        mock_parse.assert_called_once_with(source=mock_path.return_value, data=None)

    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=True)
    @mock.patch.object(AdaptiveGraph, "_upgrade_source", return_value="upgraded ttl data")
    @mock.patch.object(AdaptiveGraph, "_upgrade_data")
    @mock.patch("rdflib.Graph.parse")
    def test_version_mismatch_from_file(
        self, mock_parse, mock_upgrade_data, mock_upgrade_source, mock_mismatch, graph, tmp_path
    ):
        """Verifies _upgrade_source is called and its output forwarded to parse on a source version mismatch."""
        fake_file = tmp_path / "data.ttl"
        fake_file.write_text("original ttl data")
        result = graph.parse(source=fake_file)

        assert result is graph
        mock_mismatch.assert_called_once_with(fake_file, samm_version="1.0.0")
        mock_upgrade_source.assert_called_once_with(fake_file)
        mock_upgrade_data.assert_not_called()
        mock_parse.assert_called_with(source=None, data="upgraded ttl data")

    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=True)
    @mock.patch.object(AdaptiveGraph, "_upgrade_source")
    @mock.patch.object(AdaptiveGraph, "_upgrade_data", return_value="upgraded ttl data")
    @mock.patch("rdflib.Graph.parse")
    def test_version_mismatch_from_data(
        self, mock_parse, mock_upgrade_data, mock_upgrade_source, mock_mismatch, graph, tmp_path
    ):
        """Verifies _upgrade_data is called and its output forwarded to parse on a data version mismatch."""
        result = graph.parse(data="original ttl data")

        assert result is graph
        mock_mismatch.assert_called_once_with("original ttl data", samm_version="1.0.0")
        mock_upgrade_data.assert_called_once_with("original ttl data")
        mock_upgrade_source.assert_not_called()
        mock_parse.assert_called_with(source=None, data="upgraded ttl data")

    @mock.patch.object(AdaptiveGraph, "_upgrade_ttl_file", side_effect=RuntimeError("CLI failed"))
    @mock.patch("esmf_aspect_meta_model_python.utils.has_version_mismatch_from_input", return_value=True)
    def test_error_upgrade_failure(self, mock_version_check, mock_upgrade, graph):
        """Verifies a RuntimeError from the CLI upgrade propagates through parse."""
        with pytest.raises(RuntimeError, match="CLI failed"):
            graph.parse(data="some data")
        mock_version_check.assert_called_once_with("some data", samm_version="1.0.0")
        mock_upgrade.assert_called_once_with(mock.ANY)


@pytest.mark.parametrize(
    ("operation", "operation_name"),
    [
        ("add", "addition"),
        ("sub", "subtraction"),
        ("mul", "multiplication"),
    ],
)
class TestOperatorOverloads:
    """Tests for AdaptiveGraph operator overloads (__add__, __sub__, __mul__)."""

    def test_same_version(self, operation, operation_name, graph):
        """Verifies the SAMM version is propagated to the result when both operands share the same version."""
        g2 = AdaptiveGraph(samm_version="1.0.0")
        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=g2):
            result = getattr(graph, f"__{operation}__")(g2)

        assert isinstance(result, AdaptiveGraph)
        assert result._samm_version == "1.0.0"

    def test_add_version_conflict(self, operation, operation_name, graph):
        """Verifies ValueError is raised when the two AdaptiveGraph operands have different SAMM versions."""
        g2 = AdaptiveGraph(samm_version="2.0.0")
        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=g2):
            with pytest.raises(ValueError, match=f"SAMM version mismatch during {operation_name}."):
                getattr(graph, f"__{operation}__")(g2)

    def test_with_standard_graph(self, operation, operation_name, graph):
        """Verifies SAMM version is still propagated when the right operand is a plain rdflib.Graph."""
        g2 = Graph()
        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=graph):
            result = getattr(graph, f"__{operation}__")(g2)

        assert isinstance(result, AdaptiveGraph)
        assert result._samm_version == "1.0.0"

    def test_result_not_adaptive_graph(self, operation, operation_name, graph):
        """Verifies a non-AdaptiveGraph result is returned unchanged without SAMM version injection."""
        g2 = mock.MagicMock(spec=Graph)
        with mock.patch(f"rdflib.Graph.__{operation}__", return_value=g2):
            result = getattr(graph, f"__{operation}__")(g2)

        assert result is g2
        assert not hasattr(result, "_samm_version")
