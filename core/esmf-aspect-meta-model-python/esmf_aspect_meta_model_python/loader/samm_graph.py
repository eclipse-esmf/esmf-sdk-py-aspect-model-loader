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

from typing import List, Optional, Union

from rdflib import RDF, Graph, URIRef
from rdflib.graph import Node

from esmf_aspect_meta_model_python.base.aspect import Aspect
from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory
from esmf_aspect_meta_model_python.resolver.meta_model import AspectMetaModelResolver
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class SAMMGraph:
    """SAMM graph."""

    samm_prefix = "urn:samm:org.eclipse.esmf.samm"

    def __init__(
        self,
        graph: Graph | None = None,
        cache: Union[DefaultElementCache, None] = None,
    ):
        self._graph = graph if graph else Graph()
        self._cache = cache if cache else DefaultElementCache()
        self._samm_version = ""

        self.populate_with_meta_data()

    def __repr__(self) -> str:
        return repr(self._graph)

    def __str__(self) -> str:
        return f"SAMM {self._graph}"

    def get_rdf_graph(self) -> Graph:
        """Get RDF graph."""
        return self._graph

    def _get_samm_version_from_graph(self):
        """Get SAMM version from the graph."""
        version = ""

        for prefix, namespace in self._graph.namespace_manager.namespaces():
            if prefix == "samm":
                urn_parts = namespace.split(":")
                version = urn_parts[-1].replace("#", "")

        return version

    def get_samm_version(self):
        """Get SAMM version from the graph."""
        version = self._get_samm_version_from_graph()

        if not version:
            raise ValueError("SAMM version not found in the Graph.")
        else:
            self._samm_version = version

    def populate_with_meta_data(self):
        """Populate RDF graph with SAMM data."""
        if not self._samm_version:
            self.get_samm_version()

        meta_model_reader = AspectMetaModelResolver()
        meta_model_reader.parse(self._graph, self._samm_version)

    def get_aspect_nodes_from_graph(self) -> List[Node]:
        """Get a list of Aspect nodes from the graph."""
        nodes = []
        samm = SAMM(self._samm_version)

        # Search for Aspect elements
        for subject in self._graph.subjects(predicate=RDF.type, object=samm.get_urn(SAMM.aspect)):  # type: ignore
            nodes.append(subject)

        return nodes

    def get_base_nodes(self, aspect_urn: URIRef | str = "") -> List[Node]:
        """Get a list of base graph elements.

        :param model_pointer: pointer to the model
        :return: List of base graph elements.
        """
        base_elements: list[Node] = []

        if aspect_urn:
            base_elements += [aspect_urn if isinstance(aspect_urn, URIRef) else URIRef(aspect_urn)]
        else:
            base_elements += self.get_aspect_nodes_from_graph()

        return base_elements

    def to_python(self, aspect_urn: URIRef | str = "") -> List[Aspect]:
        """Convert SAMM graph to Python objects."""
        base_nodes = self.get_base_nodes(aspect_urn)
        if not base_nodes:
            raise ValueError(f"Could not found Aspect node by the URN {aspect_urn}.")

        model_element_factory = ModelElementFactory(self._samm_version, self._graph, self._cache)
        aspect_elements = model_element_factory.create_all_graph_elements(base_nodes)

        return aspect_elements

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
