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

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class Characteristic(Base, metaclass=abc.ABCMeta):
    """A Characteristic specifies a  property by describing its data type.
    Multiple classes inherit from Characteristic which describe
    the property in a more specific way (e.g. Enumeration or Collection).
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return hasattr(subclass, PropertyFunc.fget_name(cls.data_type))

    @property
    def data_type(self) -> DataType:
        raise NotImplementedError
