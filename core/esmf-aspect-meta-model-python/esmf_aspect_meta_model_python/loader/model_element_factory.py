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
import logging
import re

from typing import Dict, Optional, Tuple

import rdflib

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.loader import instantiator
from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache, DeferredReference
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase, T
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC
from esmf_aspect_meta_model_python.vocabulary.unit import UNIT

_logger = logging.getLogger(__name__)

# Matches the boundary in a camelCase/PascalCase identifier where an underscore should be inserted
# to convert it to snake_case (e.g. "dataType" -> "data_type", "AspectInstantiator" -> "aspect_instantiator").
_CAMEL_TO_SNAKE_PATTERN = re.compile(r"(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])")


def _camel_to_snake(name: str) -> str:
    """Converts a camelCase/PascalCase identifier to snake_case.

    Args:
        name (str): The camelCase or PascalCase name to convert.

    Returns:
        str: The snake_case representation of ``name``.
    """
    return _CAMEL_TO_SNAKE_PATTERN.sub(r"_\g<0>", name).lower()


class ModelElementFactory:
    """Aspect model element factory.

    Central class that handles the instantiation of model elements. The responsibility for different groups of model
    elements (e.g., aspect, characteristic) is delegated to instantiator classes.
    """

    def __init__(
        self,
        meta_model_version: str,
        aspect_graph: rdflib.Graph,
        cache: DefaultElementCache,
    ):
        """Initializes the model element factory with meta model version, aspect graph, and cache.

        Args:
            meta_model_version (str): The meta model version string.
            aspect_graph (rdflib.Graph): The RDF graph representing the aspect model.
            cache (DefaultElementCache): The cache for element instances and cycle handling.
        """
        self._samm = SAMM(meta_model_version)
        self._sammc = SAMMC(meta_model_version)
        self._unit = UNIT(meta_model_version)
        self._meta_model_version = meta_model_version
        self._aspect_graph = aspect_graph
        self._cache = cache

        self._instantiators: Dict[str, InstantiatorBase] = {}

    def create_aspect(self, aspect_node: Node) -> Optional[Base]:
        """Creates an aspect model element for the given aspect node.

        Args:
            aspect_node (Node): The RDF node representing the aspect.

        Returns:
            Optional[Base]: The created aspect instance, or None if deferred.
        """
        aspect_instance = self._cache.get(str(aspect_node))
        if aspect_instance is None:
            aspect_instance = self.create_element(aspect_node)
            self._cache.restore_cycle_references()

        return aspect_instance

    def create_all_graph_elements(self, create_nodes: list[Node]):
        """Create elements from the list of nodes, then restore any deferred cyclic references.

        Args:
            create_nodes (list[Node]): List of nodes to create elements from.

        Returns:
            list: List of Python created elements.
        """
        all_nodes = []

        for node in create_nodes:
            try:
                instance = self.create_element(node)
            except Exception as error:
                _logger.error("Could not translate the node %s to a Python object. Error: %s", node, error)
                raise error
            else:
                all_nodes.append(instance)

        # Restore any deferred cyclic references after all elements are created
        self._cache.restore_cycle_references()

        return all_nodes

    def _add_to_cache(self, instance):
        """Adds an instance to the cache if it is a Base element.

        Args:
            instance: The instance to add to the cache.
        """
        if isinstance(instance, Base):
            self._cache.resolve_instance(instance)

    def create_element(
        self,
        element_node: Node,
        parent_obj: Optional[Node] = None,
        attr_name: Optional[Node] = None,
    ) -> Optional[Base]:
        """Create or retrieve a model element for the given node, handling cycles and deferring cyclic references.

        Args:
            element_node (Node): Node in the aspect graph that represents the needed element.
            parent_obj (Optional[Node]): Parent node (for deferred reference, if a cycle is detected).
            attr_name (Optional[Node]): SAMM predicate pointing from the parent to this element (for
                deferred reference, if a cycle is detected).

        Returns:
            Optional[Base]: An instance of the element with all the child attributes, or None if deferred.
        """
        # Cycle detection: if node is in active path, defer reference restoration
        if self._cache.is_in_active_path(element_node):
            if parent_obj and attr_name:
                # The SAMM predicate name is camelCase (e.g. "dataType"), but the corresponding
                # Python attribute is snake_case (e.g. "data_type"). Convert it so the deferred
                # reference targets the correct attribute / backing field on restoration.
                resolver_attr_name = self._to_snake_case(self._samm.get_name(attr_name))
                if not resolver_attr_name:
                    raise ValueError(
                        f"Cannot resolve attribute name for {attr_name} in SAMM vocabulary. "
                        f"Cannot defer reference for node {element_node}."
                    )
                else:
                    self._cache.add_deferred_reference(
                        DeferredReference(
                            parent_obj,
                            resolver_attr_name,
                            str(element_node),
                        )
                    )

            else:
                raise ValueError(
                    f"Cannot defer reference for node {element_node} without parent object and attribute name."
                )

            instance = None
        else:
            # If already instantiated, return from cache
            cached_instance = self._cache.get(str(element_node))
            if cached_instance is not None:
                instance = cached_instance
            else:
                self._cache.add_to_active_path(element_node)
                element_type = self._get_element_type(element_node)
                instantiator_class = self._instantiators.get(element_type, self._create_instantiator(element_type))
                instance = instantiator_class.get_instance(element_node)
                self._add_to_cache(instance)
                self._cache.remove_from_active_path(element_node)

        return instance

    @staticmethod
    def _to_snake_case(name: Optional[str]) -> Optional[str]:
        """Converts a camelCase SAMM predicate name to a snake_case Python attribute name.

        Example: "dataType" -> "data_type", "preferredNames" -> "preferred_names".

        Args:
            name (Optional[str]): The camelCase name to convert.

        Returns:
            Optional[str]: The snake_case name, or None if the input is None.
        """
        if name is None:
            return None

        return _camel_to_snake(name)

    def _get_element_type(self, element_node: Optional[Node]) -> str:
        """Gets the element type of a node and returns it.

        Args:
            element_node (Optional[Node]): The RDF node to determine the type for.

        Returns:
            str: The determined element type.
        """
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
        """Creates the right instantiator for a given element type and adds it to the dictionary.

        Args:
            element_type (str): Type of a model element that should be created.

        Returns:
            InstantiatorBase[T]: The instantiator that can create a given model element.
        """
        module_name, class_name = self.get_instantiator_path(element_type)
        module = importlib.import_module(module_name)
        instantiator_class = getattr(module, class_name)
        instantiator_object: InstantiatorBase[T] = instantiator_class(self)
        self._instantiators[element_type] = instantiator_object

        return instantiator_object

    def get_instantiator_path(self, element_type: str) -> Tuple[str, str]:
        """Formats the module path and the class name for the needed instantiator.

        Args:
            element_type (str): Type of a model element.

        Returns:
            Tuple[str, str]:
                - Path to the module with the instantiator class
                    (e.g., esmf_aspect_meta_model_python.loader.instantiator.aspect_instantiator)
                - Name of the instantiator class (e.g., AspectInstantiator)
        """
        class_name = f"{element_type}Instantiator"

        # converts the class name (e.g. AspectInstantiator) to lowercase with
        # underscore (e.g. aspect_instantiator)
        module_name = _camel_to_snake(class_name)

        return f"{instantiator.__name__}.{module_name}", class_name

    def get_samm(self) -> SAMM:
        """Returns the SAMM vocabulary instance."""
        return self._samm

    def get_sammc(self) -> SAMMC:
        """Returns the SAMMC vocabulary instance."""
        return self._sammc

    def get_unit(self) -> UNIT:
        """Returns the UNIT vocabulary instance."""
        return self._unit

    def get_meta_model_version(self) -> str:
        """Returns the meta model version string."""
        return self._meta_model_version

    def get_aspect_graph(self) -> rdflib.Graph:
        """Returns the aspect RDF graph."""
        return self._aspect_graph
