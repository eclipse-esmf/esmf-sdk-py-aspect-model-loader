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

from os.path import exists, join
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from rdflib import Graph

from esmf_aspect_meta_model_python.resolver.base import ResolverInterface


class LocalFileResolver(ResolverInterface):
    """Local storage aspect model file resolver."""

    samm_namespace_prefix = "samm"

    def __init__(self):
        super().__init__()

        self.file_path = None

    @staticmethod
    def validate_file(file_path: Union[str, Path]):
        """Validate a SAMM file.

        :param file_path: path to the file
        """
        if not exists(file_path):
            raise FileNotFoundError(f"Could not find a file {file_path}")

    def read(self, file_path: Union[str, Path]) -> Graph:
        """
        Read an RDF graph stored in the local file.

        This method takes a string with a path to the file with RDF graph description in a serialization format
        (such as Turtle, XML, or JSON-LD) and converts it into an RDF graph object.

        Args:
            file_path (str): A string with path to the file with RDF graph description.

        Returns:
            RDFGraph: An object representing the RDF graph constructed from the input data.
        """
        self.file_path = file_path

        self.validate_file(self.file_path)
        self.graph = Graph()
        self.graph.parse(self.file_path)

        return self.graph

    @staticmethod
    def _parse_namespace(prefix_namespace: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse the prefix namespace string.

        :param prefix_namespace: namespace string of the specific prefix
        :return namespace_specific_str: dir of the namespace
        :return version: version of the model
        """
        namespace_specific_str = None
        version = None

        namespace_info = prefix_namespace.split(":")
        if len(namespace_info) == 4:
            urn, namespace_id, namespace_specific_str, version = namespace_info

            if urn == "urn" and namespace_id == "samm":
                if namespace_specific_str == "org.eclipse.esmf.samm":
                    namespace_specific_str = None
                    version = None
                else:
                    version = version.replace("#", "")

        return namespace_specific_str, version

    def _get_dirs_for_advanced_loading(self, file_path: str) -> List[str]:
        """Get directories from graph namespaces for advanced loading.

        :param file_path: str path to the main file
        :return: list of str path for further advanced files loading
        """
        paths_for_advanced_loading = []
        base_path = Path(file_path).parents[2]

        namespaces = self.graph.namespace_manager.namespaces()
        for prefix, namespace in namespaces:
            namespace_specific_str, version = self._parse_namespace(namespace)
            if namespace_specific_str and version:
                paths_for_advanced_loading.append(join(base_path, namespace_specific_str, version))

        return paths_for_advanced_loading

    def _get_dependency_folders(self, file_path: str) -> List[str]:
        """Get dependency folders from file description.

        :param file_path: path to the model file
        :return: list of dependency folders
        """
        if file_path != self.file_path:
            self.graph.parse(file_path, format="turtle")

        dependency_folders = self._get_dirs_for_advanced_loading(file_path)

        return dependency_folders

    @staticmethod
    def _get_additional_files_from_dir(file_path: str) -> List[str]:
        """Get additional files from specific directory.

        :param file_path: path list to the turtle files
        :return: list of the additional turtle files
        """
        additional_files = []

        if not exists(file_path):
            raise NotADirectoryError(f"Directory not found: {file_path}")

        for additional_file_path in Path(file_path).glob("*.ttl"):
            additional_files.append(str(additional_file_path))

        return additional_files

    def _get_dependency_files(
        self,
        file_dependencies: Dict[str, List[str]],
        folder_dependencies: Dict[str, List[str]],
        file_path: str,
    ) -> Dict[str, List[str]]:
        """Get dependency files with folder dependencies.

        :param file_dependencies: dict with dependency by file name
        :param folder_dependencies: dict with dependency by folder name
        :param file_path: path to the base file
        :return: collected dependencies for the file by its name
        """
        file_dependencies[file_path] = self._get_dependency_folders(file_path)
        for folder in file_dependencies[file_path]:
            if folder not in folder_dependencies:
                folder_dependencies[folder] = self._get_additional_files_from_dir(folder)

        files = set()
        for tmp in folder_dependencies.values():
            files.update(tmp)

        for file_path in files:
            if file_path not in file_dependencies:
                try:
                    self._get_dependency_files(file_dependencies, folder_dependencies, file_path)
                except Exception as error:
                    print(f"Could not parse file {file_path}\nError: {error}")
                    raise

        return file_dependencies

    def prepare_aspect_model(self, graph: Graph):
        """Parse namespaces from the Aspect model.

        :param graph: RDF Graph
        """
        self.graph = graph
        file_dependencies: Dict[str, List[str]] = {}
        folder_dependencies: Dict[str, List[str]] = {}

        self._get_dependency_files(file_dependencies, folder_dependencies, self.file_path)
