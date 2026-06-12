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
from esmf_aspect_meta_model_python.impl.default_property import DefaultProperty
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class PropertyInstantiator(InstantiatorBase[Property]):
    def _create_instance(self, element_node: Node) -> Property:
        """Instantiate a property by eagerly resolving all attributes.

        Handles three property node shapes: direct reference, blank node, and blank node with extends.

        Args:
            element_node (Node): The RDF node representing the property.
        Returns:
            Property: The created Property instance.
        Raises:
            ValueError: If the property node shape is not allowed.
        """
        if isinstance(element_node, URIRef):
            return self._create_property_direct_reference(element_node)

        elif isinstance(element_node, BNode):
            if self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.property)) is not None:
                return self._create_property_blank_node(element_node)
            elif self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.extends)) is not None:
                return self._create_property_with_extends(element_node)

        raise ValueError("The syntax of the property is not allowed.")

    def _create_property_direct_reference(self, element_node: URIRef) -> Property:
        """Construct a DefaultProperty instance with all attributes eagerly resolved.

        Args:
            element_node (URIRef): The RDF node representing the property.
        Returns:
            Property: The created DefaultProperty instance.
        """
        characteristic = self._get_child(element_node, self._samm.get_urn(SAMM.characteristic), required=True)
        example_value = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.example_value))

        return DefaultProperty(
            meta_model_base_attributes=self._get_base_attributes(element_node),
            characteristic=characteristic,
            example_value=example_value,
        )

    def _create_property_blank_node(self, element_node: BNode) -> Property:
        """Handle a blank node holding a reference to the property and having additional attributes.

        All attributes are eagerly resolved.

        Args:
            element_node (BNode): The blank RDF node representing the property.
        Returns:
            Property: The created DefaultProperty instance.
        Raises:
            ValueError: If the property node cannot be find.
        """
        property_node = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.property))
        if not property_node:
            raise ValueError(f"Could not find property for the node {element_node}")

        optional_node = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.optional))
        not_in_payload_node = self._aspect_graph.value(
            subject=element_node, predicate=self._samm.get_urn(SAMM.not_in_payload)
        )
        payload_name = self._get_child(element_node, self._samm.get_urn(SAMM.payload_name))
        characteristic = self._get_child(
            property_node,  # type: ignore
            self._samm.get_urn(SAMM.characteristic),
            required=True,
        )
        example_value = self._aspect_graph.value(
            subject=property_node,
            predicate=self._samm.get_urn(SAMM.example_value),
        )

        return DefaultProperty(
            meta_model_base_attributes=self._get_base_attributes(property_node),
            characteristic=characteristic,
            example_value=example_value,
            optional=optional_node is not None,
            not_in_payload=not_in_payload_node is not None,
            payload_name=payload_name,
        )

    def _create_property_with_extends(self, element_node: BNode) -> Property:
        """Construct a DefaultPropertyWithExtends instance with all attributes eagerly resolved.

        Args:
            element_node (BNode): The blank RDF node representing the property with extends.
        Returns:
            Property: The created DefaultProperty instance (with extends).
        """
        payload_name = self._get_child(element_node, self._samm.get_urn(SAMM.payload_name))
        extends = self._get_child(element_node, self._samm.get_urn(SAMM.extends), required=True)
        characteristic = self._get_child(
            element_node,
            self._samm.get_urn(SAMM.characteristic),
            required=True,
        )
        example_value = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.example_value))

        return DefaultProperty(
            meta_model_base_attributes=self._get_base_attributes(element_node),
            characteristic=characteristic,
            example_value=example_value,
            extends=extends,
            payload_name=payload_name,
        )
