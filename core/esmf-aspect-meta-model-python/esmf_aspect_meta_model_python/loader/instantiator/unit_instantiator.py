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

from typing import List
from rdflib.term import Node
from rdflib import URIRef

from esmf_aspect_meta_model_python.base.quantity_kind import QuantityKind
from esmf_aspect_meta_model_python.base.unit import Unit
from esmf_aspect_meta_model_python.impl.default_quantity_kind import DefaultQuantityKind
from esmf_aspect_meta_model_python.impl.default_unit import DefaultUnit
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class UnitInstantiator(InstantiatorBase[Unit]):
    def _create_instance(self, element_node: Node) -> Unit:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        symbol = self.__get_unit_attribute_as_string(element_node, self._samm.get_urn(SAMM.symbol))

        code = self.__get_unit_attribute_as_string(element_node, self._samm.get_urn(SAMM.common_code))

        reference_unit = self.__get_unit_attribute_as_string(element_node, self._samm.get_urn(SAMM.reference_unit))

        conversion_factor = self.__get_unit_attribute_as_string(element_node, self._samm.get_urn(SAMM.numeric_conversion_factor))

        quantity_kinds: List[QuantityKind] = []
        quantity_kind_nodes = self._aspect_graph.objects(subject=element_node, predicate=self._samm.get_urn(SAMM.quantity_kind))

        quantity_kinds.extend(self.instantiate_quantity_kind(quantity_kind_node) for quantity_kind_node in quantity_kind_nodes)

        return DefaultUnit(meta_model_base_attributes, symbol, code, reference_unit, conversion_factor, set(quantity_kinds))

    def instantiate_quantity_kind(self, quantity_kind_subject: Node) -> QuantityKind:
        meta_model_base_attributes = self._get_base_attributes(quantity_kind_subject)
        return DefaultQuantityKind(meta_model_base_attributes)

    def __get_unit_attribute_as_string(self, unit_subject: Node, attribute: URIRef) -> str:
        attribute_value = self._aspect_graph.value(unit_subject, predicate=attribute)
        if attribute_value is not None:
            attribute_value = attribute_value.toPython()
        return attribute_value
