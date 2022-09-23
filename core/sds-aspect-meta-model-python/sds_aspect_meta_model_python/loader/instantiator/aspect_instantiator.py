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

import rdflib  # type: ignore
from rdflib.term import Node

from sds_aspect_meta_model_python.base.aspect import Aspect
from sds_aspect_meta_model_python.base.operation import Operation
from sds_aspect_meta_model_python.base.property import Property
from sds_aspect_meta_model_python.impl.default_aspect import DefaultAspect
from sds_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from sds_aspect_meta_model_python.base.event import Event
from sds_aspect_meta_model_python.vocabulary.BAMM import BAMM


class AspectInstantiator(InstantiatorBase[Aspect]):
    def _create_instance(self, element_node: Node) -> Aspect:
        """creates an instance of an aspect with the aspect graph"""
        meta_model_base_attributes = self._get_base_attributes(element_node)

        if not isinstance(element_node, rdflib.URIRef):
            raise TypeError("An Aspect needs to be defined as a named node.")

        properties: List[Property] = self._get_list_children(element_node, self._bamm.get_urn(BAMM.properties))
        operations: List[Operation] = self._get_list_children(element_node, self._bamm.get_urn(BAMM.operations))
        events: List[Event] = self._get_list_children(element_node, self._bamm.get_urn(BAMM.events))
        is_collection_aspect = False

        return DefaultAspect(meta_model_base_attributes, properties, operations, events, is_collection_aspect)
