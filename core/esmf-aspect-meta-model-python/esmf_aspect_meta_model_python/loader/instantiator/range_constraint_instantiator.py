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

from rdflib import URIRef
from rdflib.term import Node

from esmf_aspect_meta_model_python.base.bound_definition import BoundDefinition
from esmf_aspect_meta_model_python.base.contraints.range_constraint import RangeConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_range_constraint import DefaultRangeConstraint
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class RangeConstraintInstantiator(InstantiatorBase[RangeConstraint]):
    def _create_instance(self, element_node: Node) -> RangeConstraint:
        meta_model_base_attributes = self._get_base_attributes(element_node)

        min_value = self.__get_min_value(element_node)

        max_value = self.__get_max_value(element_node)

        lower_bound_definition = self.__get_lower_bound_definition(element_node, min_value)

        upper_bound_definition = self.__get_upper_bound_definition(element_node, max_value)

        return DefaultRangeConstraint(
            meta_model_base_attributes,
            min_value,
            max_value,
            lower_bound_definition,
            upper_bound_definition,
        )

    def __get_upper_bound_definition(self, element_node, max_value):
        upper_bound_definition_value = self._aspect_graph.value(
            subject=element_node,
            predicate=self._sammc.get_urn(SAMMC.upper_bound_definition),
        )
        if upper_bound_definition_value is not None:
            return RangeConstraintInstantiator.__get_bound_definition(upper_bound_definition_value)

        return BoundDefinition.OPEN if max_value is None else BoundDefinition.AT_MOST

    def __get_lower_bound_definition(self, element_node, min_value):
        lower_bound_definition_value = self._aspect_graph.value(
            subject=element_node,
            predicate=self._sammc.get_urn(SAMMC.lower_bound_definition),
        )
        if lower_bound_definition_value is not None:
            return RangeConstraintInstantiator.__get_bound_definition(lower_bound_definition_value)

        return BoundDefinition.OPEN if min_value is None else BoundDefinition.AT_LEAST

    def __get_max_value(self, element_node):
        max_value = self._aspect_graph.value(subject=element_node, predicate=self._sammc.get_urn(SAMMC.max_value))
        if max_value is not None:
            max_value = max_value.toPython()
        return max_value

    def __get_min_value(self, element_node):
        min_value = self._aspect_graph.value(subject=element_node, predicate=self._sammc.get_urn(SAMMC.min_value))
        if min_value is not None:
            min_value = min_value.toPython()
        return min_value

    @staticmethod
    def __get_bound_definition(bound_definition_value: URIRef) -> BoundDefinition:
        bound_definition_value_string = bound_definition_value.toPython()
        bound_definition_start_index = bound_definition_value_string.index("#") + 1
        bound_definition_string = bound_definition_value_string[bound_definition_start_index:]
        return BoundDefinition[bound_definition_string]
