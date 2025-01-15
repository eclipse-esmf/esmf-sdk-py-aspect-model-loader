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
    """Default Aspect class."""

    LIST_ATTR_NAMES = BaseImpl.LIST_ATTR_NAMES + ["properties", "operations", "events"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        properties: List[Property],
        operations: List[Operation],
        events: List[Event],
        is_collection_aspect: bool,
    ):
        super().__init__(meta_model_base_attributes)
        self._properties = properties
        self._operations = operations
        self._events = events
        self._is_collection_aspect = is_collection_aspect
        self._set_parent_element_on_child_elements()

    def _set_parent_element_on_child_elements(self) -> None:
        """Set a parent element on child elements."""
        for aspect_property in self._properties:
            aspect_property.append_parent_element(self)

        for operation in self._operations:
            operation.append_parent_element(self)

        for event in self._events:
            event.append_parent_element(self)

    @property
    def operations(self) -> List[Operation]:
        """Operations."""
        return self._operations

    @property
    def properties(self) -> List[Property]:
        """Properties."""
        return self._properties

    @property
    def events(self) -> List[Event]:
        """Events."""
        return self._events

    @property
    def is_collection_aspect(self) -> bool:
        """Is a collection aspect flag."""
        return self._is_collection_aspect
