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

from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, TypeVar

import rdflib

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC

if TYPE_CHECKING:
    # Only import the module during type checking and not during runtime.
    # Conditional imports are often classified as code smells but here
    # it is the only solution that allows consistent type hinting and avoids circular imports.
    # Do not remove this import even if it is marked as unused.
    from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory

T = TypeVar("T")


class InstantiatorBase(Generic[T], metaclass=abc.ABCMeta):
    """Base class for all instantiators, providing references and helper methods.

    This class is generic and holds a type variable T. Every inheriting class replaces the type variable
    with the responsible meta model element type.
    """

    def __init__(self, model_element_factory: "ModelElementFactory"):
        """Initializes the instantiator with references to the model element factory and related resources.

        Args:
            model_element_factory (ModelElementFactory): The factory to delegate instantiation of child elements.
        """
        self._model_element_factory = model_element_factory
        self._samm = model_element_factory.get_samm()
        self._sammc = model_element_factory.get_sammc()
        self._unit = model_element_factory.get_unit()
        self._meta_model_version = model_element_factory.get_meta_model_version()
        self._aspect_graph: rdflib.Graph = model_element_factory.get_aspect_graph()

        # Storage of all generated instances to prevent multiple instantiation of the same element.
        self._existing_instances: Dict[str, T] = {}

    def get_instance(self, element_node: Node) -> T:
        """Returns a model instance of type T, creating it if necessary.

        Args:
            element_node (Node): Node in the aspect graph representing the element.

        Returns:
            T: An instance of the model element.
        """
        element_urn = RdfHelper.to_python(element_node)
        instance = self._existing_instances.get(element_urn)

        if not instance:
            instance = self._create_instance(element_node)
            self._existing_instances[element_urn] = instance

        return instance

    @abc.abstractmethod
    def _create_instance(self, element_node: Node) -> T:
        """Creates an instance of the given element and returns it.

        Args:
            element_node (Node): Node in the aspect graph representing the element.

        Returns:
            T: An instance of the model element.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError

    def _get_base_attributes(self, element_subject: Node) -> MetaModelBaseAttributes:
        """Creates an object with the base information of an element.

        Args:
            element_subject (Node): Element of the graph where the information should be extracted.

        Returns:
            MetaModelBaseAttributes: Object that wraps all the information (samm_version, urn, name, preferred_names,
            descriptions, see).
        """
        return MetaModelBaseAttributes.from_meta_model_element(
            element_subject,
            self._aspect_graph,
            self._samm,
            self._meta_model_version,
        )

    def _get_child(self, parent_subject: Node, child_predicate, required=False):
        """Searches for a child node of a parent node and returns an instance of it.

        The child can either be a Literal (e.g., a String) or a sub-element (e.g., Characteristic).

        Args:
            parent_subject (Node): Node in the aspect graph of the parent.
            child_predicate: Predicate that points from the parent to the child.
            required (bool, optional): Whether the child is mandatory. Defaults to False.

        Returns:
            Any: An instance of the child if it exists or None if the child does not exist and is not required.

        Raises:
            ValueError: If the child is required but does not exist.
        """
        child_subject = self._aspect_graph.value(subject=parent_subject, predicate=child_predicate)

        if child_subject is None and required:
            raise ValueError(f"Child {child_predicate} is required for element {RdfHelper.to_python(parent_subject)}")
        elif child_subject is None:  # not required
            return None
        elif isinstance(child_subject, rdflib.Literal):
            return RdfHelper.to_python(child_subject)
        else:
            return self._model_element_factory.create_element(child_subject, parent_subject, attr_name=child_predicate)

    def _get_list_children(self, element_subject: Node, list_predicate: rdflib.URIRef) -> list:
        """Extracts all children of an RDF list from the given element and returns a list of the instances.

        Used for samm:properties, samm:operations, and samm:events.

        Args:
            element_subject (Node): Element of the graph that has properties as children (e.g., aspect or entity).
            list_predicate (rdflib.URIRef): Predicate pointing from the parent to the list.

        Returns:
            list: A list of the instantiated elements.
        """
        children = []
        list_node = self._aspect_graph.value(subject=element_subject, predicate=list_predicate)
        children_nodes = RdfHelper.get_rdf_list_values(list_node, self._aspect_graph)

        for child_node in children_nodes:
            child: Any = self._model_element_factory.create_element(
                child_node, element_subject, attr_name=list_predicate
            )
            if child:
                children.append(child)

        return children

    def _get_data_type(self, element_node: Node) -> Optional[DataType]:
        """Gets the data type of a characteristic from the aspect graph.

        This method would better fit in the characteristic instantiator, but generics prevent inheritance.

        Args:
            element_node (Node): Node of the aspect graph representing the characteristic.

        Returns:
            Optional[DataType]: Data type object or None.
        """
        element_characteristic_node = self._aspect_graph.value(
            subject=element_node,
            predicate=self._sammc.get_urn(SAMMC.element_characteristic),
        )

        if element_characteristic_node:
            # some characteristics (Collection, List, TimeSeries, etc.) may have
            # an attribute "element_characteristic". If it is given, then take
            # the data type of the element_characteristic.
            data_type_node = self._aspect_graph.value(
                subject=element_characteristic_node,
                predicate=self._samm.get_urn(SAMM.data_type),
            )

            if not data_type_node:
                data_type_node = self._aspect_graph.value(
                    subject=element_characteristic_node,
                    predicate=rdflib.RDF.type,
                )
        else:
            data_type_node = self._aspect_graph.value(
                subject=element_node,
                predicate=self._samm.get_urn(SAMM.data_type),
            )

        data_type_element: Optional[DataType] = None
        if data_type_node:
            instance = self._model_element_factory.create_element(
                data_type_node, element_node, attr_name=self._samm.get_urn(SAMM.data_type)
            )

            if isinstance(instance, DataType):
                data_type_element = instance

        return data_type_element
