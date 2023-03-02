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

import abc
from typing import List

from esmf_aspect_meta_model_python.base.event import Event
from esmf_aspect_meta_model_python.base.operation import Operation
from esmf_aspect_meta_model_python.base.structure_element import StructureElement
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class Aspect(StructureElement, metaclass=abc.ABCMeta):
    """
    An aspect is the root class for a digital twin. It has a number of
    properties and operations. An Aspect Model is described in a RDF Turtle.
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, Aspect.operations, Aspect.events, Aspect.is_collection_aspect) and issubclass(subclass, StructureElement)

    @property
    def operations(self) -> List[Operation]:
        raise NotImplementedError

    @property
    def events(self) -> List[Event]:
        raise NotImplementedError

    @property
    def is_collection_aspect(self) -> bool:
        return False
