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

from typing import List

from esmf_aspect_meta_model_python.base.aspect import Aspect
from esmf_aspect_meta_model_python.base.event import Event
from esmf_aspect_meta_model_python.base.operation import Operation
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultAspect(Aspect, BaseImpl):
    """Default implementation of an aspect in the meta model.

    Represents an aspect with properties, operations, events, and a collection aspect flag.
    """

    LIST_ATTR_NAMES: List[str] = BaseImpl.LIST_ATTR_NAMES + ["properties", "operations", "events"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        properties: List[Property],
        operations: List[Operation],
        events: List[Event],
        is_collection_aspect: bool,
    ):
        """Initializes a DefaultAspect instance.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            properties (List[Property]): The list of properties for this aspect.
            operations (List[Operation]): The list of operations for this aspect.
            events (List[Event]): The list of events for this aspect.
            is_collection_aspect (bool): Flag indicating if this is a collection aspect.
        """
        super().__init__(meta_model_base_attributes)

        self._properties = properties
        self._operations = operations
        self._events = events
        self._is_collection_aspect = is_collection_aspect
        self._set_parent_element_on_child_elements()

    def _set_parent_element_on_child_elements(self) -> None:
        """Sets this aspect as the parent element on all child elements (properties, operations, events)."""
        for aspect_property in self._properties:
            aspect_property.append_parent_element(self)

        for operation in self._operations:
            operation.append_parent_element(self)

        for event in self._events:
            event.append_parent_element(self)

    @property
    def operations(self) -> List[Operation]:
        """Returns the list of operations for this aspect.

        Returns:
            List[Operation]: The operations defined for this aspect.
        """
        return self._operations

    @property
    def properties(self) -> List[Property]:
        """Returns the list of properties for this aspect.

        Returns:
            List[Property]: The properties defined for this aspect.
        """
        return self._properties

    @property
    def events(self) -> List[Event]:
        """Returns the list of events for this aspect.

        Returns:
            List[Event]: The events defined for this aspect.
        """
        return self._events

    @property
    def is_collection_aspect(self) -> bool:
        """Indicates whether this aspect is a collection aspect.

        Returns:
            bool: True if this is a collection aspect, False otherwise.
        """
        return self._is_collection_aspect
