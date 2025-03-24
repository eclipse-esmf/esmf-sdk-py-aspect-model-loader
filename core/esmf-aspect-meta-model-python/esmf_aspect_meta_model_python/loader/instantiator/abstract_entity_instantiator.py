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

import rdflib  # type: ignore

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.data_types.abstract_entity import AbstractEntity
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.data_types.default_abstract_entity import DefaultAbstractEntity
from esmf_aspect_meta_model_python.loader.instantiator.complex_type_instantiator import ComplexTypeInstantiator
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class AbstractEntityInstantiator(ComplexTypeInstantiator[AbstractEntity]):
    def _create_instance(self, element_node: Node) -> AbstractEntity:
        if not isinstance(element_node, rdflib.URIRef):
            raise TypeError("An abstract entity needs to be defined as a named node.")

        self._instantiating_now.append(element_node)

        meta_model_base_attributes = self._get_base_attributes(element_node)
        extends_element = self.get_extended_element(element_node)
        extending_subjects = self.get_extending_elements(element_node)
        properties: List[Property] = self._get_list_children(element_node, self._samm.get_urn(SAMM.properties))

        self._instantiating_now.remove(element_node)
        return DefaultAbstractEntity(meta_model_base_attributes, properties, extends_element, extending_subjects)
