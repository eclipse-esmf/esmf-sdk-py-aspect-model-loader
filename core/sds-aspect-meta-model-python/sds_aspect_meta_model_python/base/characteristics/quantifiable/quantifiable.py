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
import typing

from sds_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from sds_aspect_meta_model_python.base.unit import Unit


class Quantifiable(Characteristic, metaclass=abc.ABCMeta):
    """Describes a property where the value represents a physical value.
    It can have an optional unit."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        try:
            return isinstance(subclass.unit, property)
        except AttributeError:
            return False

    @property
    def unit(self) -> typing.Optional[Unit]:
        raise NotImplementedError
