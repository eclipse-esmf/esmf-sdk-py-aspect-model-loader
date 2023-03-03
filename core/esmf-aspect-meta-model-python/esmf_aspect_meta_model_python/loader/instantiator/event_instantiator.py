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

from esmf_aspect_meta_model_python import Property
from esmf_aspect_meta_model_python.base.event import Event
from esmf_aspect_meta_model_python.impl.default_event import DefaultEvent
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class EventInstantiator(InstantiatorBase[Event]):
    def _create_instance(self, element_node: Node) -> Event:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        parameters: List[Property] = self._get_list_children(element_node, self._samm.get_urn(SAMM.parameters))
        return DefaultEvent(meta_model_base_attributes, parameters)
