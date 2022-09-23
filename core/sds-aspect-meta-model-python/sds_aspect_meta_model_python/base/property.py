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
from typing import Optional, Any

from sds_aspect_meta_model_python.base.base import Base
from sds_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from sds_aspect_meta_model_python.base.characteristics.trait import Trait
from sds_aspect_meta_model_python.base.data_types.data_type import DataType
from sds_aspect_meta_model_python.base.property_func import PropertyFunc


class Property(Base, metaclass=abc.ABCMeta):
    """Instances of this class represent either a property or an abstract
    property.
    A property describes a model element, e.g. an Aspect or an Entity.
    It has exactly one characteristic and may have an example value.

    An abstract property can only occur inside an abstract entity. It does
    not have a characteristic and can be extended by a property inside an entity.
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(
            subclass,
            Property.characteristic,
            Property.example_value,
            Property.is_abstract,
            Property.is_optional,
            Property.is_not_in_payload,
            Property.payload_name,
            Property.data_type,
            Property.effective_characteristic,
        )

    @property
    def characteristic(self) -> Optional[Characteristic]:
        raise NotImplementedError

    @property
    def example_value(self) -> Optional[Any]:
        raise NotImplementedError

    @property
    def is_abstract(self) -> bool:
        raise NotImplementedError

    @property
    def extends(self) -> Optional["Property"]:
        raise NotImplementedError

    @property
    def is_optional(self) -> bool:
        raise NotImplementedError

    @property
    def is_not_in_payload(self) -> bool:
        raise NotImplementedError

    @property
    def payload_name(self) -> str:
        raise NotImplementedError

    @property
    def data_type(self) -> Optional[DataType]:
        effective_characteristic = self.effective_characteristic
        if effective_characteristic is None:
            return None
        else:
            return effective_characteristic.data_type

    @property
    def effective_characteristic(self) -> Optional[Characteristic]:
        characteristic = self.characteristic
        if characteristic is None:
            return None
        while isinstance(characteristic, Trait):
            characteristic = characteristic.base_characteristic
        return characteristic
