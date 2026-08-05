import pathlib
import subprocess
import tempfile

from typing import Optional, Union

from rdflib import Graph

from esmf_aspect_meta_model_python import utils
from esmf_aspect_meta_model_python.constants import SAMM_VERSION
from esmf_aspect_meta_model_python.samm_cli import SammCli


class AdaptiveGraph(Graph):  # TODO: avoid double parsing when an upgrade is not performed
    """An RDF graph that can adaptively upgrade SAMM files using the SAMM CLI."""

    _samm_cli = None  # Initialize as None

    def __init__(self, samm_version: str = SAMM_VERSION, *args, **kwargs) -> None:
        """Initialize the graph with a target SAMM version used to detect and trigger upgrades."""
        super().__init__(*args, **kwargs)

        self._samm_version = samm_version

    @classmethod
    def _get_samm_cli(cls) -> SammCli:
        """Get or create the SammCli instance (lazy initialization)."""
        if cls._samm_cli is None:
            cls._samm_cli = SammCli()

        return cls._samm_cli

    def _upgrade_ttl_file(self, file_path: pathlib.Path) -> str:
        """Run SAMM CLI prettyprint to upgrade a TTL file to the latest version."""
        try:
            return self._get_samm_cli().prettyprint(str(file_path), capture=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"SAMM CLI failed for {file_path}:\n{e.stdout}\n{e.stderr}") from e

    def _upgrade_source(self, source_path: pathlib.Path) -> str:
        """Log a mismatch warning for a file source and delegate to _upgrade_ttl_file."""
        print(f"[INFO] SAMM version mismatch detected in {source_path}. Upgrading...")

        return self._upgrade_ttl_file(source_path)

    def _upgrade_data(self, data: str | bytes) -> str:
        """Write inline data to a temp TTL file, upgrade it via SAMM CLI, then delete the temp file."""
        print(  # TODO: improve logging
            f"[INFO] SAMM version mismatch detected in provided data (target v{self._samm_version}) Upgrading..."
        )

        with tempfile.NamedTemporaryFile("wb", suffix=".ttl", delete=False) as tmp:
            tmp.write(data.encode("utf-8") if isinstance(data, str) else data)
            tmp_path = pathlib.Path(tmp.name)

        try:
            return self._upgrade_ttl_file(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def set_samm_version(self, samm_version: str) -> None:
        """Set the SAMM version for this graph."""
        self._samm_version = samm_version

    def parse(  # type: ignore[override]
        self,
        *,
        source: Optional[str | pathlib.Path] = None,
        data: Optional[str | bytes] = None,
        **kwargs,
    ) -> "AdaptiveGraph":
        """
        Parse a TTL file into this graph, upgrading via SAMM CLI if version mismatch detected.

        If a SAMM version mismatch is detected, the TTL file will be upgraded using the SAMM CLI prettyprint
        before parsing into this graph.

        Args:
            source: Path to the TTL file as pathlib.Path or str.
            data: RDF content as string or bytes.
            **kwargs: Additional arguments passed to rdflib.Graph.parse().

        Returns:
            self (AdaptiveGraph): The current graph instance with parsed data.

        Raises:
            RuntimeError: If the SAMM CLI fails during the upgrade process.
            ValueError: If neither 'source' nor 'data' is provided, or if both are provided.
        """
        if (source is None) == (data is None):
            raise ValueError("Either 'source' or 'data' must be provided.")

        if source:
            input_source = source = pathlib.Path(source)
            upgrade_method = self._upgrade_source
        else:
            input_source = data  # type: ignore[assignment]
            upgrade_method = self._upgrade_data  # type: ignore[assignment]

        if utils.has_version_mismatch_from_input(input_source, samm_version=self._samm_version):
            data = upgrade_method(input_source)
            source = None

        super().parse(source=source, data=data, **kwargs)

        return self

    def __add__(self, other: Union["Graph", "AdaptiveGraph"]) -> "AdaptiveGraph":
        """Override addition to propagate SAMM version to the resulting graph."""
        retval = super().__add__(other)

        if isinstance(retval, AdaptiveGraph):
            if isinstance(other, AdaptiveGraph) and other._samm_version != self._samm_version:
                raise ValueError("SAMM version mismatch during addition.")

            retval.set_samm_version(self._samm_version)

        return retval  # type: ignore[return-value]

    def __sub__(self, other: Union["Graph", "AdaptiveGraph"]) -> "AdaptiveGraph":
        """Override subtraction to propagate SAMM version to the resulting graph."""
        retval = super().__sub__(other)

        if isinstance(retval, AdaptiveGraph):
            if isinstance(other, AdaptiveGraph) and other._samm_version != self._samm_version:
                raise ValueError("SAMM version mismatch during subtraction.")

            retval.set_samm_version(self._samm_version)

        return retval  # type: ignore[return-value]

    def __mul__(self, other: Union["Graph", "AdaptiveGraph"]) -> "AdaptiveGraph":
        """Override multiplication to propagate SAMM version to the resulting graph."""
        retval = super().__mul__(other)

        if isinstance(retval, AdaptiveGraph):
            if isinstance(other, AdaptiveGraph) and other._samm_version != self._samm_version:
                raise ValueError("SAMM version mismatch during multiplication.")

            retval.set_samm_version(self._samm_version)

        return retval  # type: ignore[return-value]
