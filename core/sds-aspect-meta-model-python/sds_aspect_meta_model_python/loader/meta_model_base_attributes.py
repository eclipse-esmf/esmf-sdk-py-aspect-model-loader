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

from typing import Optional, List, Dict
from collections.abc import Iterable
import rdflib  # type: ignore
from rdflib.term import Node

from .rdf_helper import RdfHelper
from ..vocabulary.BAMM import BAMM


class MetaModelBaseAttributes:
    """A Wrapper object that holds all information of a Base object: bamm_version, urn, name, preferred_names,
    descriptions, see"""

    def __init__(self, meta_model_version: str, urn: Optional[str], name: str, preferred_names: Dict[str, str], descriptions: Dict[str, str], see: List[str]):
        self.meta_model_version = meta_model_version
        self.urn = urn
        self.name = name
        self.preferred_names = preferred_names
        self.descriptions = descriptions
        self.see = see

    @staticmethod
    def from_meta_model_element(meta_model_element: Node, aspect_graph: rdflib.Graph, bamm: BAMM, meta_model_version: str) -> "MetaModelBaseAttributes":
        """
        Extracts all the given base information of an element (bamm_version, urn, name,
         preferred_name, descriptions and see) and wraps it into a object of type BaseAttributes
        Args:
            meta_model_element:  URI of the node in the aspect graph representing the element
            aspect_graph: graph that represents the whole aspect
            bamm: namespace including bamm keywords used for aspect graph navigation
            meta_model_version: version of the bamm used in URNs

        Returns:
            A wrapper object with all the element attributes included
        """
        preferred_names = MetaModelBaseAttributes.__get_language_strings(meta_model_element, aspect_graph, bamm.get_urn(BAMM.preferred_name))
        descriptions = MetaModelBaseAttributes.__get_language_strings(meta_model_element, aspect_graph, bamm.get_urn(BAMM.description))
        see = MetaModelBaseAttributes.__get_attribute_value_list(meta_model_element, aspect_graph, bamm.get_urn(BAMM.see))
        urn: Optional[str] = None
        name: str = ""

        if meta_model_version == "1.0.0":
            name_result = aspect_graph.value(subject=meta_model_element, predicate=bamm.get_urn(BAMM.name))
            if name_result is not None:
                name = name_result.toPython()

        elif isinstance(meta_model_element, rdflib.BNode):
            name = MetaModelBaseAttributes.__create_default_name(meta_model_element, aspect_graph, bamm)

            return MetaModelBaseAttributes(meta_model_version, None, name, preferred_names, descriptions, see)

        if isinstance(meta_model_element, rdflib.URIRef):
            urn = meta_model_element.toPython()
            if urn is not None:
                name = MetaModelBaseAttributes.__get_name_from_urn(urn)

            return MetaModelBaseAttributes(meta_model_version, urn, name, preferred_names, descriptions, see)

        raise TypeError(
            "Unexpected type. Get MetaModelBaseAttributes.from_meta_model_element \
            can't handle this type."
        )

    @staticmethod
    def __create_default_name(meta_model_element: rdflib.BNode, aspect_graph, bamm) -> str:
        """Model elements that are defined as a blank node do not have a URI
        to identify. Therefore it is not possible to extract a name. This method
        generates an alternative name depending on the parent or the extended element.
        """
        extends_element = aspect_graph.value(subject=meta_model_element, predicate=bamm.get_urn(BAMM.extends))
        if isinstance(extends_element, rdflib.URIRef):
            return f"extending_{bamm.get_name(extends_element)}"

        parent_name, predicate_name, parent_index = RdfHelper.find_named_parent(meta_model_element, aspect_graph)

        result = f"{BAMM.get_name(parent_name)}_{BAMM.get_name(predicate_name)}"
        if parent_index != 0:
            result += f"_{str(parent_index)}"
        return result

    @staticmethod
    def __get_name_from_urn(urn: str) -> str:
        """
        Extracts the name of a model element from its urn and returns it.
        Args:
            urn: string in the format
        Returns:
            the extracted name as a string
        Examples:
            urn:bamm:io.openmanufacturing:aspect-model:TestAspect:1.0.0#testProperty -> testProperty
            urn:bamm:io.openmanufacturing:aspect-model:TestAspect:1.0.0 -> TestAspect
        """
        split_urn = urn.split("#")
        if len(split_urn) == 2:
            # urn:bamm:io.openmanufacturing:aspect-model:TestAspect:1.0.0#testProperty
            return split_urn[1]
        # urn:bamm:io.openmanufacturing:aspect-model:TestAspect:1.0.0
        split_urn = urn.split(":")
        return split_urn[-2]

    @staticmethod
    def __get_language_strings(meta_model_element: Node, aspect_graph: rdflib.Graph, bamm_attribute: rdflib.URIRef) -> Dict[str, str]:
        """Generates a Mapping of language codes to strings.
        The strings represent e.g. descriptions or preferred names

        Arguments:
            meta_model_element: URI of the node in the aspect graph representing the parent element
            aspect_graph: rdf graph that represents the whole aspect
            bamm_attribute: URN of the attribute type: e.g.
                "urn:bamm:io.openmanufacturing:meta-model:1.0.0#description"
        Returns:
            a dictionary mapping language strings on the values
        """

        language_string_generator: Iterable[Node] = aspect_graph.objects(subject=meta_model_element, predicate=bamm_attribute)

        return {language_string.language: language_string.value for language_string in language_string_generator}  # type: ignore

    @staticmethod
    def __get_attribute_value_list(meta_model_element: Node, aspect_graph: rdflib.Graph, bamm_attribute: rdflib.URIRef) -> List[str]:
        """
        generates a List of strings from a attribute that can have multiple values e.g. the attribute see.

        Arguments:
            meta_model_element: URI of the node in the aspect graph representing the parent element
            aspect_graph: rdf graph that represents the whole aspect
            bamm_attribute:URN of the attribute type: e.g.
                "urn:bamm:io.openmanufacturing:meta-model:1.0.0#see"

        Returns:
            a list of strings
        """
        value_generator: Iterable[Node] = aspect_graph.objects(subject=meta_model_element, predicate=bamm_attribute)
        return [value.toPython() for value in value_generator]  # type: ignore
