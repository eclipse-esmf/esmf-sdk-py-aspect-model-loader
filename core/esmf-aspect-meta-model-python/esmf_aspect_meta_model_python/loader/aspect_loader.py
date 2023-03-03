#  Copyright (c) 2022 Robert Bosch Manufacturing Solutions GmbH
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
from typing import Optional, Union

import rdflib  # type: ignore

from esmf_aspect_meta_model_python.base.aspect import Aspect
from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory
from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
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
        """
        creates an aspect object with all the including properties and operations with the
            turtle file
        :param file_path: path to the turtle file. Can be either a string or a Path object
        :return: instance of the aspect
        """
        return self.load_aspect_model_from_multiple_files([file_path])

    def load_aspect_model_from_multiple_files(self, file_paths: list[Union[str, Path]], aspect_urn: rdflib.URIRef | str = "") -> Aspect:
        """creates the aspect specified in urn with all the including properties and operations
        with the turtle files after merge them. an initialize a cached memory to store all
        instance to make querying them more efficient

        Args:
            file_paths (list[Union[str, Path]]): path/string list to the turtle files.

        Returns:
            Aspect: instance of the aspect
        """

        self._cache.reset()
        aspect_graph = rdflib.Graph()

        for file_path in file_paths:
            if isinstance(file_path, Path):
                file_path = str(file_path)
            aspect_graph.parse(file_path, format="turtle")

        meta_model_version = self.__extract_samm_version(aspect_graph)

        if aspect_urn == "":
            samm = SAMM(meta_model_version)
            aspect_urn = aspect_graph.value(predicate=rdflib.RDF.type, object=samm.get_urn(SAMM.aspect))

        if aspect_urn is not rdflib.URIRef:
            aspect_urn = rdflib.URIRef(aspect_urn)

        AspectMetaModelResolver.resolve_meta_model(aspect_graph, meta_model_version)
        model_element_factory = ModelElementFactory(meta_model_version, aspect_graph, self._cache)

        return model_element_factory.create_element(aspect_urn)  # type: ignore

    def __extract_samm_version(self, aspect_graph: rdflib.Graph) -> str:
        """searches the aspect graph for the currently used version of the SAMM and returns it."""
        version = ""
        for prefix, namespace in aspect_graph.namespace_manager.namespaces():
            if prefix == "samm":
                urn_parts = namespace.split(":")
                version_part = urn_parts[len(urn_parts) - 1]
                version = version_part.replace("#", "")
                return version
        return version

    def find_by_name(self, element_name: str) -> list[Base]:
        """Find a specific model element by name, and returns the found elements

        Args:
            name (str): name or pyload of element

        Returns:
            list[Base]: list of found elements
        """
        return self._cache.get_by_name(element_name)

    def find_by_urn(self, urn: str) -> Optional[Base]:
        """Find a specific model element, and returns it or undefined.

        Args:
            urn (str): urn of the model element

        Returns:
            Optional[Base]: return found element or None
        """
        return self._cache.get_by_urn(urn)

    def determine_access_path(self, base_element_name: str) -> list[list[str]]:
        """search for the element in cache first then call "determine_element_access_path"
            for every found element

        Args:
            base_element_name (str): name of element

        Returns:
            list[list[str]]: list of paths found to access the respective value.
        """
        paths: list[list[str]] = []
        base_element_list = self.find_by_name(base_element_name)
        for element in base_element_list:
            paths.extend(self.determine_element_access_path(element))

        return paths

    def determine_element_access_path(self, base_element: Base) -> list[list[str]]:
        """Determine the path to access the respective value in the Aspect JSON object.

        Args:
            base_element (Base): Element for determine the path

        Returns:
            list[list[str]]: list of paths found to access the respective value.
        """
        path: list[list[str]] = []
        if isinstance(base_element, Property):
            if hasattr(base_element, "payload_name") and base_element.payload_name is not None:  # type: ignore
                path.insert(0, [base_element.payload_name])  # type: ignore
            else:
                path.insert(0, [base_element.name])

        return self.__determine_access_path(base_element, path)

    def __determine_access_path(self, base_element: Base, path: list[list[str]]) -> list[list[str]]:
        if base_element is None or base_element.parent_elements is None or len(base_element.parent_elements) == 0:

            return path

        # in case of multiple parent get the number of additional parents and
        # clone the existing paths
        path.extend(path[0] for _ in range(len(base_element.parent_elements) - 1))

        for index, parent in enumerate(base_element.parent_elements):
            if isinstance(parent, Property):
                path_segment = ""
                if hasattr(parent, "payload_name") and parent.payload_name is not None:  # type: ignore
                    path_segment = parent.payload_name  # type: ignore
                else:
                    path_segment = parent.name

                if (len(path[index]) > 0 and path[index][0] != path_segment) or len(path[0]) == 0:
                    path[index].insert(0, path_segment)

            self.__determine_access_path(parent, path)  # type: ignore
        return path
