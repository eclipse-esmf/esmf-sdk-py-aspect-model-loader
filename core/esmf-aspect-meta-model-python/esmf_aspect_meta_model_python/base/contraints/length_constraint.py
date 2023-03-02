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
from typing import Optional

from esmf_aspect_meta_model_python.base.contraints.constraint import Constraint
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class LengthConstraint(Constraint, metaclass=abc.ABCMeta):
    """
    The LengthConstraint can be used to restrict two types of Characteristics:
    - It can restrict a string-like value in length of the value.
    - It can restrict a collection in the number of elements.
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, LengthConstraint.min_value, LengthConstraint.max_value)

    @property
    def min_value(self) -> Optional[int]:
        raise NotImplementedError

    @property
    def max_value(self) -> Optional[int]:
        raise NotImplementedError
