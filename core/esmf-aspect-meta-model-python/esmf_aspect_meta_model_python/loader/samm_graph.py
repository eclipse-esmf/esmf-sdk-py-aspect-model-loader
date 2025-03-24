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
    """Class representing the SAMM graph and its operations."""

    samm_namespace_prefix = "samm"

    def __init__(self):
        self.rdf_graph = Graph()
        self.samm_graph = Graph()
        self._cache = DefaultElementCache()

        self.samm_version = None
        self.aspect = None
        self.model_elements = None
        self._samm = None
        self._reader = None

    def __str__(self) -> str:
        """Object string representation."""
        str_data = "SAMMGraph"
        if self.samm_version:
            str_data += f" v{self.samm_version}"

        return str_data

    def __repr__(self) -> str:
        """Object representation."""
        return (
            f"<SAMMGraph identifier={id(self)} (<class 'esmf_aspect_meta_model_python.loader.samm_graph.SAMMGraph'>)>"
        )

    def _get_rdf_graph(self, input_data: Union[str, Path], input_type: Optional[str] = None):
        """Read the RDF graph from the given input data.

        This method initializes the `InputHandler` with the provided input data and type,
        retrieves the reader, and reads the RDF graph into `self.rdf_graph`.

        Args:
            input_data (Union[str, Path]): The input data to read the RDF graph from. This can be a file path or a str.
            input_type (Optional[str]): The type of the input data. If not provided, the type will be inferred.

        Returns:
            None
        """
        self._reader = InputHandler(input_data, input_type).get_reader()
        self.rdf_graph = self._reader.read(input_data)

    def _get_samm_version_from_rdf_graph(self) -> str:
        """Extracts the SAMM version from the RDF graph.

        This method searches through the RDF graph namespaces to find a prefix that indicates the SAMM version.

        Returns:
            str: The SAMM version as a string extracted from the graph. Returns an empty string if no version
                 can be conclusively identified.
        """
        version = ""

        for prefix, namespace in self.rdf_graph.namespace_manager.namespaces():
            if prefix == self.samm_namespace_prefix:
                urn_parts = namespace.split(":")
                version = urn_parts[-1].replace("#", "")

        return version

    def _get_samm_version(self):
        """Retrieve and set the SAMM version from the RDF graph.

        This method extracts the SAMM version from the RDF graph and assigns it to the `samm_version` attribute.
        If the SAMM version is not found, it raises a ValueError.

        Raises:
            ValueError: If the SAMM version is not found in the RDF graph.
        """
        self.samm_version = self._get_samm_version_from_rdf_graph()

        if not self.samm_version:
            raise ValueError(
                f"SAMM version number was not found in graph. Could not process RDF graph {self.rdf_graph}."
            )

    def _get_samm(self):
        """Initialize the SAMM object with the current SAMM version."""
        self._samm = SAMM(self.samm_version)

    def _get_samm_graph(self):
        """Parse SAMM graph base data.

        This method uses the AspectMetaModelResolver to populate samm_graph with info about SAMM elements
        based on the current SAMM version.
        """
        AspectMetaModelResolver().parse(self.samm_graph, self.samm_version)

    def parse(self, input_data: Union[str, Path], input_type: Optional[str] = None):
        """Parse the RDF graph and initialize SAMM elements.

        This method reads the RDF graph from the given input data, retrieves and sets the SAMM version,
        initializes the SAMM object, and populates the SAMM graph with base data.

        Args:
            input_data (Union[str, Path]): The input data to read the RDF graph from.
                This can be a file path or a string.
            input_type (Optional[str]): The type of the input data. If not provided, the type will be inferred.

        Returns:
            SAMMGraph: The instance of the SAMMGraph with the parsed data.
        """
        self._get_rdf_graph(input_data, input_type)
        self._get_samm_version()
        self._get_samm()
        self._get_samm_graph()

        return self

    def get_aspect_urn(self) -> Node:
        """Retrieves the URN pointing to the main aspect node of the RDF graph.

        This method searches the RDF graph for the node with predicate RDF.type and object a SAMM Aspect,
        The URN (Uniform Resource Name) of this node is then returned. This method assumes
        that the graph contains exactly one main aspect node.

        Returns:
            URIRef: reference to the Aspect node.
        """
        for subject in self.rdf_graph.subjects(predicate=RDF.type, object=self._samm.get_urn(self._samm.Aspect)):
            aspect_urn = subject
            break
        else:
            raise ValueError("Could not found Aspect node in the RDF graph.")

        return aspect_urn

    def _get_node_from_graph(self, node: Node) -> List[Node]:
        """Retrieve nodes from the RDF graph that match the given node type.

        Args:
            node (Node): The RDF node type to search for in the graph.

        Returns:
            List[Optional[Node]]: A list of nodes from the RDF graph that match the given node type.
        """
        return [subject for subject in self.rdf_graph.subjects(predicate=RDF.type, object=node) if subject]

    def get_all_model_elements(self) -> List[Node]:
        """Retrieve all SAMM elements from the RDF graph.

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
        """Creates a python object(s) to represent the Aspect model graph.

        This function takes an RDF graph and a URN for an Aspect node and converts it into
        a set of structured and connected Python objects that represents the Aspect model graph. The output is a
        list of Python objects derived from the RDF graph centered around the specified Aspect node.

        Args:
            rdf_graph (RDFGraph): The RDF graph from which to create the model.
            aspect_urn (str): The URN identifier for the main Aspect node in the RDF graph.

        Returns:
            list: A list of Python objects that represent the Aspect elements of the Aspect model graph.

        Examples:
            # Assuming 'graph' is a predefined RDFGraph object and 'aspect_urn' is defined:
            aspect_model = create_aspect_model_graph(graph, "urn:example:aspectNode")
            print(aspect_model)  # This prints the list of Python objects.

        Notes:
            It's crucial that the aspect_urn corresponds to a valid Aspect node within the RDF graph;
            otherwise, the function may not perform as expected.
        """
        if not self.aspect:
            aspect_urn = self.get_aspect_urn()

            graph = self.rdf_graph + self.samm_graph
            self._reader.prepare_aspect_model(graph)

            model_element_factory = ModelElementFactory(self.samm_version, graph, self._cache)
            self.aspect = model_element_factory.create_element(aspect_urn)

        return self.aspect

    def load_model_elements(self) -> list[BaseImpl]:
        """Creates a python object(s) to represent the Aspect model graph."""
        if self.model_elements is None:
            model_elements = self.get_all_model_elements()
            graph = self.rdf_graph + self.samm_graph
            self._reader.prepare_aspect_model(graph)

            model_element_factory = ModelElementFactory(self.samm_version, graph, self._cache)
            self.model_elements = model_element_factory.create_all_graph_elements(model_elements)

        return self.model_elements

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
