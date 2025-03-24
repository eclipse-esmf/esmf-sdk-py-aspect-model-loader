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

from typing import Optional

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.characteristics.collection.collection import Collection
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultCollection(DefaultCharacteristic, Collection):
    """Default Collection class."""

    SCALAR_ATTR_NAMES = DefaultCharacteristic.SCALAR_ATTR_NAMES + ["element_characteristic"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: Optional[DataType],
        element_characteristic: Optional[Characteristic],
    ):
        super().__init__(meta_model_base_attributes, data_type)
        self._element_characteristic = element_characteristic
        self._set_parent_element_on_child_element()

    def _set_parent_element_on_child_element(self) -> None:
        """Set a parent element on child elements."""
        if self._element_characteristic:
            self._element_characteristic.append_parent_element(self)

    @property
    def element_characteristic(self) -> Optional[Characteristic]:
        """Element characteristic."""
        return self._element_characteristic
