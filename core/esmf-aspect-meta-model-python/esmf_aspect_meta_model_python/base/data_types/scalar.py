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

from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class Scalar(DataType, metaclass=abc.ABCMeta):
    """Simple data type that specifies a value. The type of the
    scalar is determined by the URN e.g.
    http://www.w3.org/2001/XMLSchema#integer for an integer value ."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return hasattr(subclass, PropertyFunc.fget_name(cls.is_scalar))

    @property
    def is_scalar(self) -> bool:
        return True
