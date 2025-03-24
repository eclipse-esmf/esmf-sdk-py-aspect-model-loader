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

from typing import Any, Dict, Optional

import rdflib  # type: ignore

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.characteristics.state import State
from esmf_aspect_meta_model_python.impl.characteristics.default_state import DefaultState
from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG
from esmf_aspect_meta_model_python.loader.instantiator.enumeration_instantiator import EnumerationInstantiator
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class StateInstantiator(EnumerationInstantiator):
    def _create_instance(self, element_node: Node) -> State:
        data_type = self._get_data_type(element_node)
        if data_type is None:
            raise TypeError(DATA_TYPE_ERROR_MSG)

        meta_model_base_attributes = self._get_base_attributes(element_node)
        value_collection_node = self._aspect_graph.value(
            subject=element_node,
            predicate=self._sammc.get_urn(SAMMC.values),
        )
        value_nodes = RdfHelper.get_rdf_list_values(value_collection_node, self._aspect_graph)
        values = [self.__to_state_node_value(value_node) for value_node in value_nodes]

        defaultValue = self._aspect_graph.value(
            subject=element_node,
            predicate=self._sammc.get_urn(SAMMC.default_value),
        )
        default = self.__to_state_node_value(defaultValue)

        return DefaultState(meta_model_base_attributes, data_type, values, default)

    def __to_state_node_value(self, value_node: Optional[Node]) -> Dict:
        """
        This method instantiates one possible value of a state.
        :param value_node:  Node of the Graph that represents one state value.
        The Argument can either be a Literal or a URIRef.
        - If value_node is a Literal it will represent e.g. a string or an integer value
        - If value_node is a URIRef it will represent a value of a ComplexType
        :return: the one generated value of the state
        """
        if isinstance(value_node, rdflib.Literal):
            # value represents a simple data type
            return value_node.toPython()

        elif isinstance(value_node, rdflib.URIRef):
            # value represents a complex data type
            value = {}
            value_node_properties = self._aspect_graph.predicate_objects(value_node)
            for property_urn, property_value in value_node_properties:
                if property_urn != rdflib.RDF.type and isinstance(property_urn, str):
                    property_name = property_urn.split("#")[1]
                    actual_value: Optional[Any]
                    if self.__is_collection_value(property_urn):
                        actual_value = self.__instantiate_enum_collection(property_value)
                    else:
                        actual_value = self.__to_state_node_value(property_value)
                    value[property_name] = actual_value

            value_node_name = value_node.split("#")[1]
            value_key = self._samm.get_urn(SAMM.name).toPython()
            value[value_key] = value_node_name  # type: ignore
            return value

        else:
            # illegal node type for state value (e.g., Blank Node)
            raise TypeError(
                f"Every value of an state must either be a Literal (string, int, etc.) or "
                f"a URI reference to a ComplexType. Values of type {type(value_node).__name__} are not allowed"
            )
