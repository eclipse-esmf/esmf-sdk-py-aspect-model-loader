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

from typing import List, Optional

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.characteristics.collection.collection import Collection
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultCollection(DefaultCharacteristic, Collection):
    """Default implementation of a collection characteristic.

    Represents a collection with a specific element characteristic and optional data type.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultCharacteristic.SCALAR_ATTR_NAMES + ["element_characteristic"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: Optional[DataType],
        element_characteristic: Optional[Characteristic],
    ):
        """Initializes the DefaultCollection.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            data_type (Optional[DataType]): The data type of the collection.
            element_characteristic (Optional[Characteristic]): The characteristic of the collection's elements.
        """
        super().__init__(meta_model_base_attributes, data_type)
        self._element_characteristic = element_characteristic
        self._set_parent_element_on_child_element()

    def _set_parent_element_on_child_element(self) -> None:
        """Sets this collection as the parent element on its child element characteristic, if present."""
        if self._element_characteristic:
            self._element_characteristic.append_parent_element(self)

    @property
    def element_characteristic(self) -> Optional[Characteristic]:
        """Returns the characteristic of the collection's elements.

        Returns:
            Optional[Characteristic]: The element characteristic, or None if not set.
        """
        return self._element_characteristic

    @element_characteristic.setter
    def element_characteristic(self, element_characteristic: Characteristic) -> None:
        """Sets the characteristic for the collection's elements.

        Args:
            element_characteristic (Characteristic): The element characteristic to set.

        Raises:
            ValueError: If the provided element_characteristic is None.
        """
        if not element_characteristic:
            raise ValueError("Element characteristic cannot be None.")

        self._element_characteristic = element_characteristic
        self._set_parent_element_on_child_element()
