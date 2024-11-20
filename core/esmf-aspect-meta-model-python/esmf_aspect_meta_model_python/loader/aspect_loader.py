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

from typing import List

from rdflib import Graph, URIRef

from esmf_aspect_meta_model_python.base.aspect import Aspect
from esmf_aspect_meta_model_python.loader.samm_graph import SAMMGraph


class AspectLoader:
    """Entry point to load an aspect model. To load an aspect model from
    a turtle file call AspectLoader.load_aspect_model(file_path)

    cache strategy to cache created elements to ensure uniqueness and a fast lookup of it.
    The default cache strategy ignores inline defined elements.
    """

    def __init__(self):
        self.graph = None

    def load_aspect_model(self, rdf_graph: Graph, aspect_urn: URIRef | str = "") -> List[Aspect]:
        """
        Creates a python object(s) to represent the Aspect model graph.

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
        self.graph = SAMMGraph(graph=rdf_graph)
        loaded_aspect_model = self.graph.to_python(aspect_urn)

        # Add check that loaded_aspect_model is not empty
        # Add check that aspect_urn is ref to an Aspect node

        return loaded_aspect_model
