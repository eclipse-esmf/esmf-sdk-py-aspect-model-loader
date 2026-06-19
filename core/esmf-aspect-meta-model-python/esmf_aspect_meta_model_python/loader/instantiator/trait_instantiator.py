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

from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.constraints.constraint import Constraint
from esmf_aspect_meta_model_python.impl.characteristics.default_trait import DefaultTrait
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class TraitInstantiator(InstantiatorBase[Trait]):
    """Instantiates Trait elements from RDF nodes.

    This class provides logic to create Trait instances, extract constraints, and handle validation for traits
    from RDF graphs.
    """

    def _create_instance(self, element_node: Node) -> Trait:
        """Creates a Trait instance from the given RDF node.

        Args:
            element_node (Node): The RDF node representing the trait.

        Returns:
            Trait: The created Trait instance.

        Raises:
            ValueError: If the trait has no constraints or an element is not a Constraint.
        """
        meta_model_base_attributes = self._get_base_attributes(element_node)
        constraint_subjects = self._aspect_graph.objects(
            subject=element_node,
            predicate=self._sammc.get_urn(SAMMC.constraint),
        )

        constraints: List[Constraint] = []
        for constraint_subject in constraint_subjects:
            element = self._model_element_factory.create_element(
                constraint_subject, element_node, attr_name=self._sammc.get_urn(SAMMC.constraint)
            )
            if isinstance(element, Constraint):
                constraints.append(element)
            else:
                raise ValueError(f"Trait {element_node} has element {element} that is not a Constraint.")

        if not constraints:
            raise ValueError("Trait must have at least one constraint.")

        base_characteristic = self._get_child(
            element_node,
            self._sammc.get_urn(SAMMC.base_characteristic),
            required=True,
        )

        return DefaultTrait(meta_model_base_attributes, base_characteristic, constraints)
