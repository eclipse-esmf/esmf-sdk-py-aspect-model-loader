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

from esmf_aspect_meta_model_python.base.contraints.length_constraint import LengthConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_length_constraint import DefaultLengthConstraint
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class LengthConstraintInstantiator(InstantiatorBase[LengthConstraint]):
    def _create_instance(self, element_node: Node) -> LengthConstraint:
        meta_model_base_attributes = self._get_base_attributes(element_node)

        min_value_node = self._aspect_graph.value(subject=element_node, predicate=self._sammc.get_urn(SAMMC.min_value))
        min_value = int(RdfHelper.to_python(min_value_node)) if min_value_node else None

        max_value_node = self._aspect_graph.value(subject=element_node, predicate=self._sammc.get_urn(SAMMC.max_value))
        max_value = int(RdfHelper.to_python(max_value_node)) if max_value_node else None

        return DefaultLengthConstraint(meta_model_base_attributes, min_value, max_value)
