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

from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.default_property import DefaultProperty
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class AbstractPropertyInstantiator(InstantiatorBase[Property]):
    def _create_instance(self, element_node: Node) -> Property:
        """
        Instantiates an abstract property. It explicitly sets the
        characteristic and the example value to None.

        Abstract property nodes may occur in two different shapes.
        1) A abstract property that does not specify any of the attributes
        optional, payloadName and notInPayload is always a direct reference
        to an abstract property node.

        2) A property that specifies at least one of the attributes optional,
        payloadName or notInPayload is defined as a blank node.
        The remaining attributes (e.g., preferredName, description, etc.)
        are specified in an extra node referenced with the predicate
        samm:property.

        This method finds out which one of the two shapes occurs and chooses
        one of two methods for the instantiation.

        :param element_node: A URN to the node that represents the property.

        :return: an instance of the property
        """
        if isinstance(element_node, rdflib.URIRef):
            return self._create_property_direct_reference(element_node)
        elif isinstance(element_node, rdflib.BNode):
            return self._create_property_blank_node(element_node)
        else:
            raise ValueError("Invalid syntax for Abstract Property")

    def _create_property_direct_reference(self, element_node: rdflib.URIRef) -> Property:
        """The given node is a named node representing the property"""
        meta_model_base_attributes = self._get_base_attributes(element_node)

        example_value = self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.example_value))

        return DefaultProperty(
            meta_model_base_attributes,
            characteristic=None,
            example_value=example_value,
            abstract=True,
        )

    def _create_property_blank_node(self, element_node: rdflib.BNode) -> Property:
        """The given node is a blank node holding a reference to the property
        and having additional attributes like optional or not_in_payload"""
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

        return DefaultProperty(
            meta_model_base_attributes,
            characteristic=None,
            example_value=example_value,
            abstract=True,
            optional=optional,
            not_in_payload=not_in_payload,
            payload_name=payload_name,
        )
