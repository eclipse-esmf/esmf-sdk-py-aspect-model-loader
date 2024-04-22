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
from typing import Dict, Optional, Union

import rdflib  # type: ignore

from esmf_aspect_meta_model_python.base.aspect import Aspect
from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory
from esmf_aspect_meta_model_python.resolver.aspect_meta_model_resolver import AspectMetaModelResolver
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class AspectLoader:
    """Entry point to load an aspect model. To load an aspect model from
    a turtle file call AspectLoader.load_aspect_model(file_path)
    """

    def __init__(self) -> None:
        """
        cache strategy to cache created elements to ensure uniqueness and a fast lookup of it.
                          The default cache strategy ignores inline defined elements.
        """
        self._cache = DefaultElementCache()

    def load_aspect_model(self, file_path: Union[str, Path]) -> Aspect:
        """Load aspect model to RDF GRAPH.

        Create an aspect object with all the including properties and operations with the turtle file

        :param file_path: path to the turtle file. Can be either a string or a Path object
        :return: instance of the aspect
        """
        return self._load_aspect_model_from_multiple_files([file_path])

    @staticmethod
    def _get_additional_files_from_dir(file_path: str) -> list[str]:
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

    @staticmethod
    def _parse_namespace(prefix_namespace: str) -> tuple[Optional[str], Optional[str]]:
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
                version = version.replace("#", "")

        return namespace_specific_str, version

    def _get_dirs_for_advanced_loading(self, aspect_graph: rdflib.Graph, file_path: str) -> list[str]:
        """Get directories from graph namespaces for advanced loading.

        :param aspect_graph:rdflib.Graph
        :param file_path: str path to the main file
        :return: list of str path for further advanced files loading
        """
        paths_for_advanced_loading = []
        base_path = Path(file_path).parents[2]

        for prefix, namespace in aspect_graph.namespace_manager.namespaces():
            namespace_specific_str, version = self._parse_namespace(namespace)
            if namespace_specific_str and version:
                paths_for_advanced_loading.append(join(base_path, namespace_specific_str, version))

        return paths_for_advanced_loading

    @staticmethod
    def _prepare_file_paths(file_paths: list[Union[str, Path]]):
        """Check and prepare file paths."""
        prepared_file_paths = []

        for file_path in file_paths:
            if not exists(Path(file_path)):
                raise FileNotFoundError(f"Could not find a file {file_path}")

            prepared_file_paths.append(str(file_path))

        return prepared_file_paths

    def get_dependency_folders(self, file_path):
        """Get dependency folders from file description."""
        graph = rdflib.Graph()
        graph.parse(file_path, format="turtle")

        dependency_folders = self._get_dirs_for_advanced_loading(graph, file_path)

        return dependency_folders

    def _get_dependency_files(self, file_dependencies, folder_dependencies, file_path):
        """Get dependency files with folder dependencies."""
        file_dependencies[file_path] = self.get_dependency_folders(file_path)
        for folder in file_dependencies[file_path]:
            if folder not in folder_dependencies:
                folder_dependencies[folder] = self._get_additional_files_from_dir(folder)

        files = set()
        for tmp in folder_dependencies.values():
            files.update(tmp)

        for file_path in files:
            if file_path not in file_dependencies:
                self._get_dependency_files(file_dependencies, folder_dependencies, file_path)

        return file_dependencies

    def _get_all_dependencies(self, file_paths: list[Union[str, Path]]):
        """Get all dependency files."""
        file_dependencies: Dict[str, list[str]] = {}
        folder_dependencies: Dict[str, list[str]] = {}
        for file_path in file_paths:
            file_dependencies.update(self._get_dependency_files(file_dependencies, folder_dependencies, file_path))

        return file_dependencies

    def _get_graph(self, file_paths: list[Union[str, Path]]) -> rdflib.Graph:
        """Get RDF graph object.

        :param file_paths: list of absolute paths to the turtle files.
        :return: parsed rdflib Graph.
        """
        aspect_graph = rdflib.Graph()
        file_paths = self._prepare_file_paths(file_paths)
        for file_path in self._get_all_dependencies(file_paths):
            aspect_graph.parse(file_path, format="turtle")

        return aspect_graph

    def _load_aspect_model_from_multiple_files(
        self,
        file_paths: list[Union[str, Path]],
        aspect_urn: rdflib.URIRef | str = "",
    ) -> Aspect:
        """Load aspect model from multiple files.

        Create aspect specified in urn with all the including properties and operations with the turtle files
        after merge them. Initialize a cached memory to store all
        instance to make querying them more efficient

        :param file_paths: path/string list to the turtle files
        :param aspect_urn: urn of the Aspect property
        :return: instance of the aspect graph
        """
        self._cache.reset()
        aspect_graph = self._get_graph(file_paths)
        meta_model_version = self.__extract_samm_version(aspect_graph)

        if aspect_urn == "":
            samm = SAMM(meta_model_version)
            aspect_urn = aspect_graph.value(predicate=rdflib.RDF.type, object=samm.get_urn(SAMM.aspect))  # type: ignore

        if aspect_urn is not rdflib.URIRef:
            aspect_urn = rdflib.URIRef(aspect_urn)

        AspectMetaModelResolver.resolve_meta_model(aspect_graph, meta_model_version)
        model_element_factory = ModelElementFactory(meta_model_version, aspect_graph, self._cache)
        aspect_element = model_element_factory.create_element(aspect_urn)  # type: ignore

        return aspect_element

    @staticmethod
    def __extract_samm_version(aspect_graph: rdflib.Graph) -> str:
        """Get samm version.

        searches the aspect graph for the currently used version of the SAMM and returns it

        :param aspect_graph: RDF graph
        """
        version = ""

        for prefix, namespace in aspect_graph.namespace_manager.namespaces():
            if prefix == "samm":
                urn_parts = namespace.split(":")
                version = urn_parts[-1].replace("#", "")

        return version

    def find_by_name(self, element_name: str) -> list[Base]:
        """Find a specific model element by name, and returns the found elements

        :param element_name: name or pyload of element
        :return: list of found elements
        """
        return self._cache.get_by_name(element_name)

    def find_by_urn(self, urn: str) -> Optional[Base]:
        """Find a specific model element, and returns it or undefined.

        :param urn: urn of the model element
        :return: found element or None
        """
        return self._cache.get_by_urn(urn)

    def determine_access_path(self, base_element_name: str) -> list[list[str]]:
        """Determine the access path.

        Search for the element in cache first then call "determine_element_access_path" for every found element

        :param base_element_name: name of element
        :return: list of paths found to access the respective value.
        """
        paths: list[list[str]] = []
        base_element_list = self.find_by_name(base_element_name)
        for element in base_element_list:
            paths.extend(self.determine_element_access_path(element))

        return paths

    def determine_element_access_path(self, base_element: Base) -> list[list[str]]:
        """Determine the path to access the respective value in the Aspect JSON object.

        :param base_element: element for determine the path
        :return: list of paths found to access the respective value.
        """
        path: list[list[str]] = []
        if isinstance(base_element, Property):
            if hasattr(base_element, "payload_name") and base_element.payload_name is not None:  # type: ignore
                path.insert(0, [base_element.payload_name])  # type: ignore
            else:
                path.insert(0, [base_element.name])

        return self.__determine_access_path(base_element, path)

    def __determine_access_path(self, base_element: Base, path: list[list[str]]) -> list[list[str]]:
        """Determine access path.

        :param base_element: element for determine the path
        :return: list of paths found to access the respective value.
        """
        if base_element is None or base_element.parent_elements is None or len(base_element.parent_elements) == 0:
            return path

        # in case of multiple parent get the number of additional parents and
        # clone the existing paths
        path.extend(path[0] for _ in range(len(base_element.parent_elements) - 1))

        for index, parent in enumerate(base_element.parent_elements):
            if isinstance(parent, Property):
                if hasattr(parent, "payload_name") and parent.payload_name is not None:  # type: ignore
                    path_segment = parent.payload_name  # type: ignore
                else:
                    path_segment = parent.name

                if (len(path[index]) > 0 and path[index][0] != path_segment) or len(path[0]) == 0:
                    path[index].insert(0, path_segment)

            self.__determine_access_path(parent, path)  # type: ignore

        return path
