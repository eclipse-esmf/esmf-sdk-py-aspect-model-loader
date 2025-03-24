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

from rdflib import BNode, Node, URIRef

from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.default_property import (
    DefaultBlankProperty,
    DefaultProperty,
    DefaultPropertyWithExtends,
)
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class PropertyInstantiator(InstantiatorBase[Property]):
    def _create_instance(self, element_node: Node) -> Property:
        """
        Instantiates a property by instantiating the child characteristic and
        extracting additional attributes.

        Property Nodes may occur in three different shapes.
        1) A property that does not extend another property and does not
        specify any of the attributes optional, payloadName and notInPayload
        is always a direct reference to a property node.

        2) A property that does not extend another property and specifies
        at least one of the attributes optional, payloadName or notInPayload
        is defined as a blank node. The remaining attributes (e.g., preferredName,
        characteristic, etc.) are specified in an extra node referenced with
        the predicate samm:property.

        3) A property that extends another property is defined as a blank node.
        All attributes (e.g., characteristic, exampleValue) are specified in the
        same node.

        This method finds out which one of the three shapes occurs and chooses
        one of three methods for the instantiation.

        :param element_node: Either URN to the node or a BNode that
        represents the property.

        :return: an instance of the property
        """
        property_instance = None

        if isinstance(element_node, URIRef):
            property_instance = self._create_property_direct_reference(element_node)

        elif isinstance(element_node, BNode):
            if self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.property)) is not None:
                property_instance = self._create_property_blank_node(element_node)
            elif self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.extends)) is not None:
                property_instance = self._create_property_with_extends(element_node)

        if not property_instance:
            raise ValueError("The syntax of the property is not allowed.")

        return property_instance

    def _create_property_direct_reference(self, element_node: URIRef) -> Property:
        """The given node is a named node representing the property"""
        return DefaultProperty(
            meta_model_base_attributes=self._get_base_attributes(element_node),
            elements_factory=self._model_element_factory,
            graph_node=element_node,
        )

    def _create_property_blank_node(self, element_node: BNode) -> Property:
        """The given node is a blank node holding a reference to the property
        and having additional attributes like optional or not_in_payload."""
        property_node = self._aspect_graph.value(
            subject=element_node,
            predicate=self._samm.get_urn(SAMM.property),
        )
        if not property_node:
            raise ValueError(f"Could not find property for the node {element_node}")

        return DefaultBlankProperty(
            base_element_node=element_node,
            meta_model_base_attributes=self._get_base_attributes(property_node),
            elements_factory=self._model_element_factory,
            graph_node=property_node,
        )

    def _create_property_with_extends(self, element_node: BNode) -> Property:
        """The given node is a blank node representing a property extending
        another property."""
        return DefaultPropertyWithExtends(
            meta_model_base_attributes=self._get_base_attributes(element_node),
            elements_factory=self._model_element_factory,
            graph_node=element_node,
        )
