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

import sys
from typing import Optional, List, Union

import rdflib  # type: ignore
from rdflib import term, Graph, BNode
from rdflib.term import Node


class RdfHelper:
    @staticmethod
    def get_rdf_list_values(rdf_list: Optional[BNode], aspect_graph: Graph) -> List[term.Identifier]:
        """A collection in rdf is a binary tree. The top of the tree is a blank node.
        One predicate of the node is connected to the first element of the collection.
        The other predicate is connected to a node with the rest of the binary tree.
        This method gets all the Nodes of the collection elements by iterating the tree recursively.

        Arguments:
            rdf_list: Blank Node representing the collection
            aspect_graph: rdf graph representing the whole aspect

        Returns:
            a list of all Nodes representing the collection elements
        """
        list_elements: List[term.Identifier] = []

        first_entry: Optional[term.Identifier] = aspect_graph.value(subject=rdf_list, predicate=rdflib.RDF.first)

        if first_entry is not None:
            list_elements = [first_entry]
            remaining_entries: Optional[term.BNode] = aspect_graph.value(subject=rdf_list, predicate=rdflib.RDF.rest)
            list_elements.extend(RdfHelper.get_rdf_list_values(remaining_entries, aspect_graph))
        return list_elements

    @staticmethod
    def find_named_parent(meta_model_element: Node, aspect_graph: rdflib.Graph, counter: int = 0) -> tuple:
        """This method searches in the aspect graph for a named parent.
        If the found parent is a blank node search recursively for the
        grand parent.

        Arguments:
            meta_model_element: Node in the graph representing the child
            aspect_graph: rdf graph representing the whole aspect
            counter: indicates the recursion depth

        Returns: a tuple with
            - The node representing the named parent

            - The predicate pointing towards the child

            - A value that indicates the distance between parent and child
        """
        result: tuple = (None, None, 0)
        if counter >= sys.getrecursionlimit():
            return result

        for subject, predicate in aspect_graph.subject_predicates(object=meta_model_element):
            if isinstance(subject, rdflib.URIRef) and isinstance(predicate, rdflib.URIRef):
                result = subject, predicate, counter
            else:
                # search for grand parent
                result = RdfHelper.find_named_parent(subject, aspect_graph, counter + 1)  # type: ignore
        return result

    @staticmethod
    def to_python(to_be_python: Union[term.Identifier, Node]) -> str:
        """Converts an RDF node into a Python representation.

        Examples:
            to_python(URIRef) -> URI as string

            to_python(BNode) -> unique id as string

            to_python(Literal) -> literal as Python type (e.g., int or string)
        """
        if isinstance(to_be_python, (rdflib.URIRef, rdflib.BNode, rdflib.Graph, rdflib.Literal)):
            return to_be_python.toPython()  # type: ignore
        raise TypeError("Unknown toPython type.")
