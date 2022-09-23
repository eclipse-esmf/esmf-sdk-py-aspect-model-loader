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

from sds_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from sds_aspect_meta_model_python.base.property_func import PropertyFunc


class Either(Characteristic, metaclass=abc.ABCMeta):
    """Describes a property that has exactly one of two possible values."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, Either.left, Either.right)

    @property
    def left(self) -> Characteristic:
        raise NotImplementedError

    @property
    def right(self) -> Characteristic:
        raise NotImplementedError
