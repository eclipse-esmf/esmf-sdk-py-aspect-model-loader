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

import rdflib  # type: ignore

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.property import AbstractProperty
from esmf_aspect_meta_model_python.impl.default_property import DefaultAbstractProperty
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class AbstractPropertyInstantiator(InstantiatorBase[AbstractProperty]):
    def _create_instance(self, element_node: Node) -> AbstractProperty:
        """Instantiates an abstract property, setting characteristic and example value to None.

        Abstract property nodes may occur in two shapes:
        1) A direct reference to an abstract property node (no optional, payloadName, notInPayload attributes).
        2) A blank node with at least one of optional, payloadName, or notInPayload, referencing the property node.

        Args:
            element_node (Node): The node representing the property (URN or blank node).

        Returns:
            AbstractProperty: An instance of the abstract property.

        Raises:
            ValueError: If the node is not a valid URIRef or BNode.
        """
        if isinstance(element_node, rdflib.URIRef):
            return self._create_property_direct_reference(element_node)
        elif isinstance(element_node, rdflib.BNode):
            return self._create_property_blank_node(element_node)
        else:
            raise ValueError("Invalid syntax for Abstract Property")

    def _create_property_direct_reference(self, element_node: rdflib.URIRef) -> AbstractProperty:
        """Creates an abstract property from a named node (direct reference).

        Args:
            element_node (rdflib.URIRef): The named node representing the property.

        Returns:
            AbstractProperty: The instantiated abstract property.
        """
        meta_model_base_attributes = self._get_base_attributes(element_node)
        example_value = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.example_value))

        return DefaultAbstractProperty(
            meta_model_base_attributes,
            example_value=example_value,
            abstract=True,
        )

    def _create_property_blank_node(self, element_node: rdflib.BNode) -> AbstractProperty:
        """Creates an abstract property from a blank node with additional attributes.

        Args:
            element_node (rdflib.BNode): The blank node holding a reference to the property and extra attributes.

        Returns:
            AbstractProperty: The instantiated abstract property.
        """
        optional = (
            self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.optional)) is not None
        )
        not_in_payload = (
            self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.not_in_payload))
            is not None
        )
        payload_name = self._get_child(element_node, self._samm.get_urn(SAMM.payload_name))

        property_node = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.property))

        meta_model_base_attributes = self._get_base_attributes(property_node)  # type: ignore

        example_value = self._aspect_graph.value(
            subject=property_node,
            predicate=self._samm.get_urn(SAMM.example_value),
        )

        return DefaultAbstractProperty(
            meta_model_base_attributes,
            example_value=example_value,
            abstract=True,
            optional=optional,
            not_in_payload=not_in_payload,
            payload_name=payload_name,
        )
