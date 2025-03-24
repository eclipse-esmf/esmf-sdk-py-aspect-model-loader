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

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.quantity_kind import QuantityKind
from esmf_aspect_meta_model_python.impl.default_quantity_kind import DefaultQuantityKind
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase


class QuantityKindInstantiator(InstantiatorBase[QuantityKind]):
    def _create_instance(self, element_node: Node) -> QuantityKind:
        meta_model_base_attributes = self._get_base_attributes(element_node)

        return DefaultQuantityKind(meta_model_base_attributes)
