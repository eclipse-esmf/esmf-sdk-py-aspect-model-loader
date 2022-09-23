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
from typing import Set, Optional

from sds_aspect_meta_model_python.base.base import Base
from sds_aspect_meta_model_python.base.quantity_kind import QuantityKind
from sds_aspect_meta_model_python.base.property_func import PropertyFunc


class Unit(Base, metaclass=abc.ABCMeta):
    """A unit is used to specify the magnitude of a physical quantity.
    Examples for units are meter, millimeter, inch, or volts.
    A Unit in the BAMM
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, Unit.symbol, Unit.code, Unit.reference_unit, Unit.conversion_factor, Unit.quantity_kinds)

    @property
    def symbol(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def code(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def reference_unit(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def conversion_factor(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def quantity_kinds(self) -> Set[QuantityKind]:
        raise NotImplementedError
