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

import abc

from typing import List, Optional

import rdflib  # type: ignore

from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase, T
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class ComplexTypeInstantiator(InstantiatorBase[T], metaclass=abc.ABCMeta):
    """Abstract base class for the instantiators of Entity and AbstractEntity.
    Implements helper methods for both instantiators and holds a shared
    list of currently instantiating Entities.
    """

    _instantiating_now: List[rdflib.URIRef] = []

    def get_extended_element(self, entity_subject: rdflib.URIRef) -> Optional[str]:
        """
        gets the urn of the extends element and instantiates it if it
        has not been instantiated yet.
        Args:
            entity_subject: node of the extending element

        Returns:
            urn of the extended element
        """
        extended_element_node = self._aspect_graph.value(
            subject=entity_subject,
            predicate=self._samm.get_urn(SAMM.extends),
        )
        if extended_element_node is None:
            return None
        if extended_element_node not in self._instantiating_now:
            self._model_element_factory.create_element(extended_element_node)
        return RdfHelper.to_python(extended_element_node)

    def get_extending_elements(self, entity_subject: rdflib.URIRef) -> List[str]:
        """
        returns a list of urns of entities which extend the given entity.
        If an extending element has not been instantiated yet, instantiate it.

        This is relevant when an Entity is not connected to the aspect directly
        but extends an AbstractEntity which is connected to the aspect.

        Args:
            entity_subject: node of the extended element

        Returns:
            list of urns of the extended element
        """
        elements: List[str] = []
        all_element_subjects = self._aspect_graph.subjects(
            predicate=self._samm.get_urn(SAMM.extends),
            object=entity_subject,
        )
        for element_subject in all_element_subjects:
            if element_subject not in self._instantiating_now:
                self._model_element_factory.create_element(element_subject)
            elements.append(RdfHelper.to_python(element_subject))
        return elements
