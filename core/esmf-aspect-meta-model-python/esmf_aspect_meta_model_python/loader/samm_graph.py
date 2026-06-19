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
from typing import List, Optional, Union

from rdflib import RDF, Graph, Node

import esmf_aspect_meta_model_python.constants as const

from esmf_aspect_meta_model_python import utils
from esmf_aspect_meta_model_python.adaptive_graph import AdaptiveGraph
from esmf_aspect_meta_model_python.base.aspect import Aspect
from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory
from esmf_aspect_meta_model_python.resolver.handler import InputHandler
from esmf_aspect_meta_model_python.resolver.meta_model import AspectMetaModelResolver
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class SAMMGraph:
    """Represents the SAMM graph and provides operations for parsing and model instantiation.

    This class manages the RDF and SAMM graphs, handles parsing, and provides methods to load and query aspect models.
    """

    def __init__(self):
        """Initializes the SAMMGraph with default graphs, cache, and version information."""
        self.rdf_graph = AdaptiveGraph()
        self.samm_graph = Graph()
        self._cache = DefaultElementCache()

        self.samm_version = const.SAMM_VERSION
        self.aspect = None
        self.model_elements = None
        self._samm = None
        self._reader = None

    def __str__(self) -> str:
        """Returns a string representation of the SAMMGraph object."""
        return f"SAMMGraph v{self.samm_version}"

    def __repr__(self) -> str:
        """Returns a detailed representation of the SAMMGraph object."""
        return (
            f"<SAMMGraph identifier={id(self)} (<class 'esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph'>)>"
        )

    def _get_rdf_graph(self, input_data: Union[str, Path], input_type: Optional[str] = None):
        """Reads the RDF graph from the given input data.

        This method initializes the InputHandler with the provided input data and type, retrieves the reader,
        and reads the RDF graph into self.rdf_graph.

        Args:
            input_data (Union[str, Path]): The input data to read the RDF graph from. This can be a file path or a str.
            input_type (Optional[str]): The type of the input data. If not provided, the type will be inferred.

        Returns:
            None
        """
        self._reader = InputHandler(input_data, input_type).get_reader()
        self.rdf_graph = self._reader.read(input_data)

    def _get_samm(self):
        """Initializes the SAMM object with the current SAMM version."""
        self._samm = SAMM(self.samm_version)

    def _get_samm_graph(self):
        """Parses SAMM graph base data and populates samm_graph with SAMM elements for the current version."""
        AspectMetaModelResolver().parse(self.samm_graph, self.samm_version)

    def parse(self, input_data: Union[str, Path], input_type: Optional[str] = None):
        """Parses the RDF graph and initializes SAMM elements.

        This method reads the RDF graph from the given input data, retrieves and sets the SAMM version,
        initializes the SAMM object, and populates the SAMM graph with base data.

        Args:
            input_data (Union[str, Path]): The input data to read the RDF graph from (file path or string).
            input_type (Optional[str]): The type of the input data. If not provided, the type will be inferred.

        Returns:
            SAMMGraph: The instance of the SAMMGraph with the parsed data.
        """
        self._get_rdf_graph(input_data, input_type)
        self._get_samm()
        self._get_samm_graph()

        return self

    def get_aspect_urn(self) -> Node:
        """Retrieves the URN pointing to the main aspect node of the RDF graph.

        This method searches the RDF graph for the node with predicate RDF.type and object a SAMM Aspect.
        The URN (Uniform Resource Name) of this node is then returned. This method assumes that the graph contains
        exactly one main aspect node.

        Returns:
            Node: Reference to the Aspect node.
        """
        for subject in self.rdf_graph.subjects(predicate=RDF.type, object=self._samm.get_urn(self._samm.Aspect)):
            aspect_urn = subject
            break
        else:
            raise ValueError("Could not found Aspect node in the RDF graph.")

        return aspect_urn

    def _get_node_from_graph(self, node: Node) -> List[Node]:
        """Retrieves nodes from the RDF graph that match the given node type.

        Args:
            node (Node): The RDF node type to search for in the graph.

        Returns:
            List[Node]: A list of nodes from the RDF graph that match the given node type.
        """
        return [subject for subject in self.rdf_graph.subjects(predicate=RDF.type, object=node) if subject]

    def get_all_model_elements(self) -> List[Node]:
        """Retrieves all SAMM elements from the RDF graph.

        Returns:
            List[Node]: A list of nodes representing all model elements in the RDF graph.

        Raises:
            ValueError: If no SAMM elements are found in the RDF graph.
        """
        model_elements: List[Node] = []
        for element in self._samm.meta_model_elements:
            model_elements += self._get_node_from_graph(self._samm.get_urn(element))

        if not model_elements:
            raise ValueError("There are no SAMM elements in the RDF graph.")

        return model_elements

    def load_aspect_model(self) -> Aspect:
        """Creates Python objects to represent the Aspect model graph.

        This function takes an RDF graph and a URN for an Aspect node and converts it into a set of structured and
        connected Python objects that represent the Aspect model graph. The output is a list of Python objects derived
        from the RDF graph centered around the specified Aspect node.

        Returns:
            Aspect: The Aspect object representing the Aspect model graph.
        """
        if not self.aspect:
            aspect_urn = self.get_aspect_urn()

            graph = self.rdf_graph + self.samm_graph
            self._reader.prepare_aspect_model(graph)
            self._validate_samm_namespace_version(graph)

            model_element_factory = ModelElementFactory(self.samm_version, graph, self._cache)
            self.aspect = model_element_factory.create_aspect(aspect_urn)
            self.aspect.validate()

        return self.aspect

    def _validate_samm_namespace_version(self, graph: AdaptiveGraph) -> None:
        """Validates that the SAMM version in the graph's namespace matches the detected SAMM version.

        Args:
            graph (AdaptiveGraph): The RDF graph whose namespaces are to be validated.

        Raises:
            ValueError: If the SAMM version in the graph's namespace does not match the detected SAMM version.
        """
        for version in utils.get_samm_versions_from_graph(graph):
            if version != self.samm_version:
                raise ValueError(
                    f"SAMM version mismatch. Found '{version}', but expected '{self.samm_version}'. "
                    "Ensure all RDF files use a single, consistent SAMM version"
                )

    def _get_aspect_from_elements(self):
        """Gets and saves the Aspect element from the model elements."""
        if self.model_elements:
            for element in self.model_elements:
                if isinstance(element, Aspect):
                    self.aspect = element
                    break

    def load_model_elements(self) -> list[BaseImpl]:
        """Creates Python objects to represent all model elements in the Aspect model graph."""
        if self.model_elements is None:
            model_elements = self.get_all_model_elements()
            graph = self.rdf_graph + self.samm_graph
            self._reader.prepare_aspect_model(graph)

            model_element_factory = ModelElementFactory(self.samm_version, graph, self._cache)
            self.model_elements = model_element_factory.create_all_graph_elements(model_elements)
            for element in self.model_elements:
                element.validate()

            self._get_aspect_from_elements()

        return self.model_elements

    def find_by_name(self, element_name: str) -> list[Base]:
        """Finds model elements by name and returns the found elements.

        Args:
            element_name (str): Name or payload of the element.

        Returns:
            list[Base]: List of found elements.
        """
        return self._cache.get_by_name(element_name)

    def find_by_urn(self, urn: str) -> Optional[Base]:
        """Finds a specific model element by URN and returns it or None.

        Args:
            urn (str): URN of the model element.

        Returns:
            Optional[Base]: Found element or None.
        """
        return self._cache.get_by_urn(urn)

    def determine_access_path(self, base_element_name: str) -> list[list[str]]:
        """Determines all access paths for a given element name.

        Finds elements by name in the cache and computes all possible access paths for each found element.

        Args:
            base_element_name (str): Name of the element to search for.

        Returns:
            list[list[str]]: List of paths found to access the respective value.
        """
        paths: list[list[str]] = []
        base_element_list = self.find_by_name(base_element_name)
        for element in base_element_list:
            paths.extend(self.determine_element_access_path(element))

        return paths

    def determine_element_access_path(self, base_element: Base) -> list[list[str]]:
        """Determines the access path(s) for a given model element.

        Computes the path(s) to access the respective value in the Aspect JSON object for the provided element.

        Args:
            base_element (Base): The element for which to determine the path.

        Returns:
            list[list[str]]: List of paths found to access the respective value.
        """
        path: list[list[str]] = []
        if isinstance(base_element, Property):
            if hasattr(base_element, "payload_name") and base_element.payload_name is not None:  # type: ignore
                path.insert(0, [base_element.payload_name])  # type: ignore
            else:
                path.insert(0, [base_element.name])

        return self.__determine_access_path(base_element, path)

    def __determine_access_path(self, base_element: Base, path: list[list[str]]) -> list[list[str]]:
        """Recursively determines all access paths for a model element.

        Traverses parent elements to build all possible access paths to the given element.

        Args:
            base_element (Base): The element for which to determine the path.
            path (list[list[str]]): The current path(s) being constructed.

        Returns:
            list[list[str]]: List of paths found to access the respective value.
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
