#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from abc import ABC, abstractmethod
from typing import Any, Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType


class AbstractProperty(Base, ABC):
    """Property interface class.

    Instances of this class represent either a property or an abstract property.
    A property describes a model element, e.g. an Aspect or an Entity.
    It has exactly one characteristic and may have an example value.

    An abstract property can only occur inside an abstract entity.
    It does not have a characteristic and can be extended by a property inside an entity.
    """

    @property
    @abstractmethod
    def example_value(self) -> Optional[Any]:
        """Example value."""

    @property
    @abstractmethod
    def is_abstract(self) -> bool:
        """Is abstract flag."""

    @property
    @abstractmethod
    def extends(self) -> Optional["Property"]:
        """Extends."""

    @property
    @abstractmethod
    def is_optional(self) -> bool:
        """Is optional flag."""

    @property
    @abstractmethod
    def is_not_in_payload(self) -> bool:
        """Is not in payload class."""

    @property
    @abstractmethod
    def payload_name(self) -> str:
        """Payload name."""

    @property
    def data_type(self) -> Optional[DataType]:
        """Data type."""
        return None



class Property(AbstractProperty, ABC):
    """Property interface class.

    Instances of this class represent either a property or an abstract property.
    A property describes a model element, e.g. an Aspect or an Entity.
    It has exactly one characteristic and may have an example value.

    An abstract property can only occur inside an abstract entity.
    It does not have a characteristic and can be extended by a property inside an entity.
    """

    @property
    @abstractmethod
    def characteristic(self) -> Optional[Characteristic]:
        """Characteristic."""

    @property
    def data_type(self) -> Optional[DataType]:
        """Data type."""
        return self.effective_characteristic.data_type if self.effective_characteristic else None

    @property
    def effective_characteristic(self) -> Optional[Characteristic]:
        """Effective characteristic."""
        characteristic = None

        if self.characteristic:
            characteristic = self.characteristic
            while isinstance(characteristic, Trait):
                characteristic = characteristic.base_characteristic

        return characteristic
