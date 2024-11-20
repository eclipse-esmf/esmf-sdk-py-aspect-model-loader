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

from rdflib import RDF, Graph

from esmf_aspect_meta_model_python.resolver.base import ResolverInterface
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class DataStringResolver(ResolverInterface):
    """String aspect model presenter resolver."""

    def read(self, data_string: str):
        """
        Parses the provided data string into an RDF graph.

        This method takes a string that contains RDF graph description in a serialization format (such as Turtle, XML,
        or JSON-LD) and converts it into an RDF graph object.

        Args:
            data_string (str): A string containing RDF data. This should be in a valid RDF serialization format.

        Returns:
            RDFGraph: An object representing the RDF graph constructed from the input data.
        """
        self.graph = Graph()
        self.graph.parse(data=data_string)

        return self.graph

    def get_aspect_urn(self):
        """
        Retrieves the URN pointing to the main aspect node of the RDF graph.

        This method searches the RDF graph for the node with predicate RDF.type and object a SAMM Aspect,
        The URN (Uniform Resource Name) of this node is then returned. This method assumes
        that the graph contains exactly one main aspect node.

        Returns:
            str: The URN of the SAMM aspect node in the RDF graph.
        """
        samm = SAMM(self.get_samm_version())
        self.aspect_urn = self.graph.value(predicate=RDF.type, object=samm.get_urn(SAMM.aspect), any=False)

        return self.aspect_urn
