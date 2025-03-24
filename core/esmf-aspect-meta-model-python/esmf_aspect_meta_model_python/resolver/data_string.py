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

from rdflib import Graph

from esmf_aspect_meta_model_python.resolver.base import ResolverInterface


class DataStringResolver(ResolverInterface):
    """String aspect model presenter resolver."""

    def read(self, data_string: Union[str, Path]):
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
        self.graph.parse(data=str(data_string) if isinstance(data_string, Path) else data_string)

        return self.graph
