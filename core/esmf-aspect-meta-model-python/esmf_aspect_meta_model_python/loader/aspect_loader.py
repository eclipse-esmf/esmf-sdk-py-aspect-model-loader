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

from pathlib import Path
from typing import Union

from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
from esmf_aspect_meta_model_python.loader.samm_graph import SAMMGraph


class AspectLoader:
    """Entry point to load an aspect model. To load an aspect model from
    a turtle file call AspectLoader.load_aspect_model(file_path)

    cache strategy to cache created elements to ensure uniqueness and a fast lookup of it.
    The default cache strategy ignores inline defined elements.
    """

    def __init__(self) -> None:
        self._cache = DefaultElementCache()
        self._graph = SAMMGraph()

    def get_graph(self) -> SAMMGraph:
        """Get SAMM graph.

        :return: parsed SAMM Aspect model Graph.
        """
        return self._graph

    def get_samm_version(self) -> str:
        """Get SAMM version of the graph."""
        return self._graph.get_samm_version()

    @staticmethod
    def convert_file_path(file_path: Union[str, Path]) -> str:
        """Convert file_path to the string.

        :param file_path: path to model file
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)

        tmp_path = Path(file_path)
        if not tmp_path.exists():
            raise FileNotFoundError(f"Could not found the file {tmp_path}")

        return file_path

    def _reset_graph(self):
        """Reset graph and cache data."""
        if self._graph:
            self._graph = SAMMGraph()

        if self._cache:
            self._cache = DefaultElementCache()

    def load_aspect_model(self, file_path: Union[Path, str]):
        """Load aspect model to RDF GRAPH.

        Create an aspect object with all the including properties and operations with the turtle file

        :param file_path: path to the turtle file. Can be either a string or a Path object
        :return: instance of the aspect
        """
        file_path = self.convert_file_path(file_path)
        self._reset_graph()
        _ = self._graph.parse(file_path)
        loaded_aspect_model = self._graph.to_python()

        return loaded_aspect_model
