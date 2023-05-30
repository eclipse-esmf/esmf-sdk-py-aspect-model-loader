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

from esmf_aspect_meta_model_python.base.contraints.fixed_point_constraint import FixedPointConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_fixed_point_constraint import DefaultFixedPointConstraint
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class FixedPointConstraintInstantiator(InstantiatorBase[FixedPointConstraint]):
    def _create_instance(self, element_node: Node) -> FixedPointConstraint:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        scale = self._aspect_graph.value(subject=element_node, predicate=self._sammc.get_urn(SAMMC.scale)).toPython()
        integer = self._aspect_graph.value(subject=element_node, predicate=self._sammc.get_urn(SAMMC.integer)).toPython()
        return DefaultFixedPointConstraint(meta_model_base_attributes, scale, integer)
