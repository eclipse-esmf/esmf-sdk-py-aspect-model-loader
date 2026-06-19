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

    An abstract property can only occur inside an abstract entity.
    It does not have a characteristic and can be extended by a property inside an entity.
    """

    @property
    @abstractmethod
    def example_value(self) -> Optional[Any]:
        """Returns the example value for the property, if set.

        Returns:
            Optional[Any]: The example value, or None if not set.
        """

    @property
    @abstractmethod
    def is_abstract(self) -> bool:
        """Indicates whether the property is abstract.

        Returns:
            bool: True if the property is abstract, False otherwise.
        """

    @property
    @abstractmethod
    def extends(self) -> Optional["Property"]:
        """Returns the property that this property extends, if any.

        Returns:
            Optional[Property]: The extended property, or None if not set.
        """

    @property
    @abstractmethod
    def is_optional(self) -> bool:
        """Indicates whether the property is optional.

        Returns:
            bool: True if the property is optional, False otherwise.
        """

    @property
    @abstractmethod
    def is_not_in_payload(self) -> bool:
        """Indicates whether the property is not included in the payload class.

        Returns:
            bool: True if the property is not in the payload, False otherwise.
        """

    @property
    @abstractmethod
    def payload_name(self) -> str:
        """Returns the name of the property in the payload.

        Returns:
            str: The payload name.
        """

    @property
    def data_type(self) -> Optional[DataType]:
        """Returns the data type of the property, if available.

        Returns:
            Optional[DataType]: The data type, or None if not set.
        """
        return None


class Property(AbstractProperty, ABC):
    """Property interface class.

    A property describes a model element, e.g. an Aspect or an Entity.
    It has exactly one characteristic and may have an example value.
    """

    @property
    @abstractmethod
    def characteristic(self) -> Optional[Characteristic]:
        """Returns the characteristic of the property, if set.

        Returns:
            Optional[Characteristic]: The characteristic, or None if not set.
        """

    @property
    def data_type(self) -> Optional[DataType]:
        """Returns the data type of the property, if available.

        Returns:
            Optional[DataType]: The data type, or None if not set.
        """
        return self.effective_characteristic.data_type if self.effective_characteristic else None

    @property
    def effective_characteristic(self) -> Optional[Characteristic]:
        """Returns the effective characteristic, resolving through Trait wrappers if necessary.

        Returns:
            Optional[Characteristic]: The effective characteristic, or None if not set.
        """
        characteristic = None

        if self.characteristic:
            characteristic = self.characteristic
            while isinstance(characteristic, Trait):
                characteristic = characteristic.base_characteristic

        return characteristic
