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
from typing import List, Optional

from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc
from esmf_aspect_meta_model_python.base.structure_element import StructureElement
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType


class ComplexType(DataType, StructureElement, metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, ComplexType.all_properties, ComplexType.is_abstract_entity, ComplexType.extends, ComplexType.is_scalar)

    @property
    def all_properties(self) -> List[Property]:
        raise NotImplementedError

    @property
    def is_abstract_entity(self) -> bool:
        return False

    @property
    def extends(self) -> Optional["ComplexType"]:
        raise NotImplementedError

    @property
    def is_scalar(self) -> bool:
        return False
