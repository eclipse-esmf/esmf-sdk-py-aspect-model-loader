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

import rdflib  # type: ignore
from rdflib.term import Node

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.default_property import DefaultProperty
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


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
        if isinstance(element_node, rdflib.URIRef):
            return self._create_property_direct_reference(element_node)

        elif isinstance(element_node, rdflib.BNode):
            if self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.property)) is not None:
                return self._create_property_blank_node(element_node)
            elif self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.extends)) is not None:
                return self._create_property_with_extends(element_node)

        raise ValueError("The syntax of the property is not allowed.")

    def _create_property_direct_reference(self, element_node: rdflib.URIRef) -> Property:
        """The given node is a named node representing the property"""
        meta_model_base_attributes = self._get_base_attributes(element_node)

        characteristic: Characteristic = self._get_child(element_node, self._samm.get_urn(SAMM.characteristic), required=True)

        example_value = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.example_value))

        return DefaultProperty(meta_model_base_attributes, characteristic, example_value)

    def _create_property_blank_node(self, element_node: rdflib.BNode) -> Property:
        """The given node is a blank node holding a reference to the property
        and having additional attributes like optional or not_in_payload"""
        optional = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.optional)) is not None
        not_in_payload = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.not_in_payload)) is not None
        payload_name = self._get_child(element_node, self._samm.get_urn(SAMM.payload_name))

        property_node = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.property))

        meta_model_base_attributes = self._get_base_attributes(property_node)

        characteristic: Characteristic = self._get_child(property_node, self._samm.get_urn(SAMM.characteristic), required=True)

        example_value = self._aspect_graph.value(subject=property_node, predicate=self._samm.get_urn(SAMM.example_value))

        return DefaultProperty(
            meta_model_base_attributes, characteristic, example_value, optional=optional, not_in_payload=not_in_payload, payload_name=payload_name
        )

    def _create_property_with_extends(self, element_node: rdflib.BNode) -> Property:
        """The given node is a blank node representing a property extending
        another property."""
        payload_name = self._get_child(element_node, self._samm.get_urn(SAMM.payload_name))
        extends = self._get_child(element_node, self._samm.get_urn(SAMM.extends), required=True)

        meta_model_base_attributes = self._get_base_attributes(element_node)

        characteristic: Characteristic = self._get_child(element_node, self._samm.get_urn(SAMM.characteristic), required=True)

        example_value = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.example_value))

        return DefaultProperty(meta_model_base_attributes, characteristic, example_value, extends, payload_name=payload_name)
