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

from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.contraints.constraint import Constraint
from esmf_aspect_meta_model_python.impl.characteristics.default_trait import DefaultTrait
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.BAMMC import BAMMC


class TraitInstantiator(InstantiatorBase[Trait]):
    def _create_instance(self, element_node: Node) -> Trait:
        meta_model_base_attributes = self._get_base_attributes(element_node)

        constraint_subjects = self._aspect_graph.objects(subject=element_node, predicate=self._bammc.get_urn(BAMMC.constraint))

        constraints: List[Constraint] = [self._model_element_factory.create_element(constraint_subject) for constraint_subject in constraint_subjects]
        if not constraints:
            raise ValueError("Trait must have at least one constraint.")

        base_characteristic = self._get_child(element_node, self._bammc.get_urn(BAMMC.base_characteristic), required=True)

        return DefaultTrait(meta_model_base_attributes, base_characteristic, constraints)
