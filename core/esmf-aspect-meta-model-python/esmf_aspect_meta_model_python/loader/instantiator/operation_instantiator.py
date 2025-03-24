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

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.operation import Operation
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.default_operation import DefaultOperation
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class OperationInstantiator(InstantiatorBase[Operation]):
    def _create_instance(self, element_node: Node) -> Operation:
        """
        instantiates a single operation and adds input and output properties as children
        :param operation_subject: URI of the node representing the operation
        :return: an instance of type DefaultOperation
        """
        meta_model_base_attributes = self._get_base_attributes(element_node)

        input: List[Property] = self._get_list_children(element_node, self._samm.get_urn(SAMM.input))
        output = self._get_child(element_node, self._samm.get_urn(SAMM.output))

        return DefaultOperation(meta_model_base_attributes, input, output)
