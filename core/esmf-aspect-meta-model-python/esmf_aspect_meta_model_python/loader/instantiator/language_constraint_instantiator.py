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

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.contraints.language_constraint import LanguageConstraint
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.BAMMC import BAMMC
from esmf_aspect_meta_model_python.impl.constraints.default_language_constraint import DefaultLanguageConstraint


class LanguageConstraintInstantiator(InstantiatorBase[LanguageConstraint]):
    def _create_instance(self, element_node: Node) -> LanguageConstraint:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        language_code = self._aspect_graph.value(subject=element_node, predicate=self._bammc.get_urn(BAMMC.language_code)).toPython()
        return DefaultLanguageConstraint(meta_model_base_attributes, language_code)
