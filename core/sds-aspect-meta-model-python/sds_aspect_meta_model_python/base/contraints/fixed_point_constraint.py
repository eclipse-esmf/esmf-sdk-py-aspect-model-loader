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

from sds_aspect_meta_model_python.base.contraints.constraint import Constraint
from sds_aspect_meta_model_python.base.property_func import PropertyFunc


class FixedPointConstraint(Constraint, metaclass=abc.ABCMeta):
    """Defines the scaling factor as well as the amount of
    integral numbers for a fixed point number.
    The constraint may only be used in conjunction with Characteristics
    which use the xsd:decimal data type.
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, FixedPointConstraint.scale, FixedPointConstraint.integer)

    @property
    def scale(self) -> int:
        raise NotImplementedError

    @property
    def integer(self) -> int:
        raise NotImplementedError
