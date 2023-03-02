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

from typing import Any
from rdflib import Literal
from rdflib.term import Node

from esmf_aspect_meta_model_python.base.characteristics.structured_value import StructuredValue
from esmf_aspect_meta_model_python.impl.characteristics.default_structured_value import DefaultStructuredValue
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from esmf_aspect_meta_model_python.vocabulary.BAMMC import BAMMC


class StructuredValueInstantiator(InstantiatorBase[StructuredValue]):
    def _create_instance(self, element_node: Node) -> StructuredValue:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        data_type = self._get_data_type(element_node)

        deconstruction_rule = self._aspect_graph.value(subject=element_node, predicate=self._bammc.get_urn(BAMMC.deconstruction_rule)).toPython()

        element_nodes = self._aspect_graph.value(subject=element_node, predicate=self._bammc.get_urn(BAMMC.elements))
        element_node_list = RdfHelper.get_rdf_list_values(element_nodes, self._aspect_graph)
        elements = [self.__to_element_node_value(element_node) for element_node in element_node_list]

        if data_type is None:
            raise TypeError("Data type can't be None.")

        return DefaultStructuredValue(meta_model_base_attributes, data_type, deconstruction_rule, elements)

    def __to_element_node_value(self, element_node: Node) -> Any:
        """creates a property that is wrapped in a structured value"""
        if isinstance(element_node, Literal):
            return element_node.toPython()
        return self._model_element_factory.create_element(element_node)
