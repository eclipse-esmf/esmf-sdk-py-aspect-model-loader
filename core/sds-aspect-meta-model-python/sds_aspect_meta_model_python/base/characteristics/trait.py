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

from sds_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from sds_aspect_meta_model_python.base.property_func import PropertyFunc
from ..contraints import constraint


class Trait(Characteristic, metaclass=abc.ABCMeta):
    """Describes a property where the value is restricted by
    one or more constraints. A Trait has one base characteristic which
    describes the actual value and a number of constraints which
    restrict this value.
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, Trait.base_characteristic, Trait.constraints)

    @property
    def base_characteristic(self) -> Characteristic:
        raise NotImplementedError

    @property
    def constraints(self) -> List[constraint.Constraint]:
        raise NotImplementedError
