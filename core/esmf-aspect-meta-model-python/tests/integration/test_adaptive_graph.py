from unittest import mock

from esmf_aspect_meta_model_python.adaptive_graph import AdaptiveGraph


class TestAdaptiveGraphIntegration:
    """Integration tests for AdaptiveGraph end-to-end parse with SAMM CLI mocking."""

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._get_samm_cli")
    def test_mismatch_from_file(self, get_samm_cli_mock, tmp_path, capsys):
        """Verifies the graph is upgraded and logged when the file SAMM version mismatches."""
        file_path = tmp_path / "bad_version.ttl"
        file_path.write_text(
            """
            @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:9.9.9#> .
            samm:Aspect a samm:Aspect .
            """
        )
        samm_cli_mock = mock.MagicMock(name="samm_cli")
        samm_cli_mock.prettyprint.return_value = """
            @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:1.0.0#> .
            samm:Aspect a samm:Aspect .
            """
        get_samm_cli_mock.return_value = samm_cli_mock
        graph = AdaptiveGraph(samm_version="1.0.0")
        graph.parse(source=file_path, format="ttl")

        assert len(graph) == 1
        ns_list = list(dict(graph.namespace_manager.namespaces()).values())
        assert any("1.0.0" in str(ns) for ns in ns_list)
        assert f"[INFO] SAMM version mismatch detected in {file_path}. Upgrading..." in capsys.readouterr().out
        get_samm_cli_mock.assert_called_once()
        samm_cli_mock.prettyprint.assert_called_once_with(str(file_path), capture=True)

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._get_samm_cli")
    def test_mismatch_from_data(self, get_samm_cli_mock, tmp_path, capsys):
        """Verifies the graph is upgraded and logged when inline TTL data SAMM version mismatches."""
        bad_ttl_data = """
            @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:2.0.0#> .
            samm:Aspect a samm:Aspect .
            """
        samm_cli_mock = mock.MagicMock(name="samm_cli")
        samm_cli_mock.prettyprint.return_value = """
            @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:1.0.0#> .
            samm:Aspect a samm:Aspect .
            """
        get_samm_cli_mock.return_value = samm_cli_mock
        graph = AdaptiveGraph(samm_version="1.0.0")
        graph.parse(data=bad_ttl_data, format="ttl")

        assert len(graph) == 1
        ns_list = list(dict(graph.namespace_manager.namespaces()).values())
        assert any("1.0.0" in str(ns) for ns in ns_list)
        assert (
            "[INFO] SAMM version mismatch detected in provided data (target v1.0.0) Upgrading..."
            in capsys.readouterr().out
        )
        get_samm_cli_mock.assert_called_once()
        samm_cli_mock.prettyprint.assert_called_once_with(mock.ANY, capture=True)

    @mock.patch("esmf_aspect_meta_model_python.adaptive_graph.AdaptiveGraph._get_samm_cli")
    def test_integration_version_match_no_upgrade(self, get_samm_cli_mock, tmp_path, capsys):
        """Verifies no upgrade is performed and no warning is logged when the file SAMM version matches."""
        file_path = tmp_path / "good_version.ttl"
        file_path.write_text(
            """
            @prefix samm: <urn:samm:org.eclipse.esmf.samm:aspect:1.0.0#> .
            samm:Aspect a samm:Aspect .
            """
        )
        samm_cli_mock = mock.MagicMock(name="samm_cli")
        get_samm_cli_mock.return_value = samm_cli_mock
        graph = AdaptiveGraph(samm_version="1.0.0")
        graph.parse(source=file_path, format="ttl")

        assert len(graph) == 1
        samm_cli_mock.prettyprint.assert_not_called()
        assert capsys.readouterr().out == ""
