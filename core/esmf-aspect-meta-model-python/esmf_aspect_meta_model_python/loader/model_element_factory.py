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

import importlib
import re

from typing import Dict, Optional, Tuple, Type, Union

import rdflib

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.loader import instantiator
from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase, T
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC
from esmf_aspect_meta_model_python.vocabulary.unit import UNIT


class ModelElementFactory:
    """Aspect model element factory.

    Central class that handles the instantiation of model elements.
    The responsibility for different groups of model elements (e.g. aspect, characteristic)
    is delegated to instantiator classes.
    """

    def __init__(
        self,
        meta_model_version: str,
        aspect_graph: rdflib.Graph,
        cache: DefaultElementCache,
    ):
        self._samm = SAMM(meta_model_version)
        self._sammc = SAMMC(meta_model_version)
        self._unit = UNIT(meta_model_version)
        self._meta_model_version = meta_model_version
        self._aspect_graph = aspect_graph
        self._cache = cache

        self._instantiators: Dict[str, InstantiatorBase] = {}

    def create_all_graph_elements(self, create_nodes: list[Node]):
        """Create elements from the list of nodes.

        Create python classes for the given list of nodes.

        :param create_nodes: List of nodes to create elements from.
        :return: List of python created elements.
        """
        all_nodes = []

        for node in create_nodes:
            try:
                instance = self.create_element(node)
            except Exception as error:
                print(f"Could nod translate the node {node} to a Python object. Error: {error}")
                raise error
            else:
                all_nodes.append(instance)

        return all_nodes

    def _add_to_cache(self, instance):
        """Add an instance to the cache."""
        if isinstance(instance, Base):
            self._cache.resolve_instance(instance)

    def create_element(self, element_node: Node) -> Union[Type[Base], DataType, Type[DataType]]:
        """
        searches for the right instantiator to create a new instance or
         find an existing one.
         If the instantiator does not exists, a new one is created.
         Then a copy of the instance will saved in the cache.

        Args:
            element_node: node in the aspect graph that represents the
            needed element

        Returns:
            an instance of the element with all the child attributes
        """
        element_type = self._get_element_type(element_node)
        instantiator_class = self._instantiators.get(element_type, self._create_instantiator(element_type))
        instance = instantiator_class.get_instance(element_node)
        self._add_to_cache(instance)

        return instance

    def _get_element_type(self, element_node: Optional[Node]) -> str:
        """Gets the element type of a node and returns it."""
        element_type_urn = self._aspect_graph.value(subject=element_node, predicate=rdflib.RDF.type)
        element_type = self._samm.get_name(element_type_urn)

        if element_type is None:
            # If the node does not have a type it can be one of the following elements:
            # 1. A property that extends another property
            # 2. A property or abstract property that is defined as a blank node
            # 3. A scalar
            if self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.extends)):
                element_type = "Property"
            elif self._aspect_graph.value(subject=element_node, predicate=self._samm.get_urn(SAMM.property)):
                # property is a blank node and can either be a property or
                # an abstract property. Therefore, get the type of the subnode.
                property_node = self._aspect_graph.value(
                    subject=element_node,
                    predicate=self._samm.get_urn(SAMM.property),
                )
                element_type = self._get_element_type(property_node)
            else:
                element_type = "Scalar"

        return element_type

    def _create_instantiator(self, element_type: str) -> InstantiatorBase[T]:
        """
        creates the right instantiator for a given element type and
        adds it to the dictionary
        Args:
            element_type: Type of a model element that should be created

        Returns:
            The instantiator that can create a given model element
        """
        module_name, class_name = self.get_instantiator_path(element_type)
        module = importlib.import_module(module_name)
        instantiator_class = getattr(module, class_name)
        instantiator_object: InstantiatorBase[T] = instantiator_class(self)
        self._instantiators[element_type] = instantiator_object

        return instantiator_object

    def get_instantiator_path(self, element_type: str) -> Tuple[str, str]:
        """
        formats the module path and the class name for the
        needed instantiator.
        Args:
            element_type: Type of a model element

        Returns: tuple with:
            - path to the module with the instantiator class
            (e.g. esmf_aspect_meta_model_python.loader.instantiator.aspect_instantiator)

            - name of the instantiator class (e.g. AspectInstantiator)
        """
        class_name = f"{element_type}Instantiator"

        # converts the class name (e.g. AspectInstantiator) to lowercase with
        # underscore (e.g. aspect_instantiator)
        module_name = re.sub(r"(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])", r"_\g<0>", class_name).lower()
        return f"{instantiator.__name__}.{module_name}", class_name

    def get_samm(self) -> SAMM:
        return self._samm

    def get_sammc(self) -> SAMMC:
        return self._sammc

    def get_unit(self) -> UNIT:
        return self._unit

    def get_meta_model_version(self) -> str:
        return self._meta_model_version

    def get_aspect_graph(self) -> rdflib.Graph:
        return self._aspect_graph
