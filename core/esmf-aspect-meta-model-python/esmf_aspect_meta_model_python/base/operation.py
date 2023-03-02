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

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class Operation(Base, metaclass=abc.ABCMeta):
    """Meta Model element which represents an operation of an aspect.
    An operation has a number of input properties and one optional output
    property.
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, Operation.input_properties, Operation.output_property)

    @property
    def input_properties(self) -> List[Property]:
        raise NotImplementedError

    @property
    def output_property(self) -> Optional[Property]:
        raise NotImplementedError
