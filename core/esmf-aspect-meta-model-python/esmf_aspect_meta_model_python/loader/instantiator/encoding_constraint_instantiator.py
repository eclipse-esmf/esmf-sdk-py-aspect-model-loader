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

from esmf_aspect_meta_model_python.base.contraints.encoding_constraint import EncodingConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_encoding_constraint import DefaultEncodingConstraint
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class EncodingConstraintInstantiator(InstantiatorBase[EncodingConstraint]):
    def _create_instance(self, element_node: Node) -> EncodingConstraint:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        value = RdfHelper.to_python(
            self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.value)),
        )
        value = value.split("#")[1]
        return DefaultEncodingConstraint(meta_model_base_attributes, value)
