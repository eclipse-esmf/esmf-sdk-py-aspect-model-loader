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

from typing import Any

from rdflib import Literal
from rdflib.term import Node

from esmf_aspect_meta_model_python.base.characteristics.structured_value import StructuredValue
from esmf_aspect_meta_model_python.impl.characteristics.default_structured_value import DefaultStructuredValue
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class StructuredValueInstantiator(InstantiatorBase[StructuredValue]):
    """Instantiates StructuredValue elements from RDF nodes.

    This class provides logic to create StructuredValue instances, extract elements, and handle both simple and complex
    structured value types from RDF graphs.
    """

    def _create_instance(self, element_node: Node) -> StructuredValue:
        """Creates a StructuredValue instance from the given RDF node.

        Args:
            element_node (Node): The RDF node representing the structured value.

        Returns:
            StructuredValue: The created StructuredValue instance.
        """
        data_type = self._get_data_type(element_node)
        if not data_type:
            raise ValueError(f"StructuredValue {element_node} must have a data type.")

        meta_model_base_attributes = self._get_base_attributes(element_node)
        deconstruction_rule = RdfHelper.to_python(
            self._aspect_graph.value(
                subject=element_node,
                predicate=self._sammc.get_urn(SAMMC.deconstruction_rule),
            )
        )
        element_nodes = self._aspect_graph.value(subject=element_node, predicate=self._sammc.get_urn(SAMMC.elements))
        element_node_list = RdfHelper.get_rdf_list_values(element_nodes, self._aspect_graph)
        elements = [self.__to_element_node_value(element_node) for element_node in element_node_list if element_node]

        return DefaultStructuredValue(meta_model_base_attributes, data_type, deconstruction_rule, elements)

    def __to_element_node_value(self, element_node: Node) -> Any:
        """Creates a property that is wrapped in a structured value.

        Args:
            element_node (Node): The RDF node representing the element.

        Returns:
            Any: The value of the element, either as a Python primitive or a created element instance.
        """
        if isinstance(element_node, Literal):
            return element_node.toPython()

        return self._model_element_factory.create_element(element_node)
