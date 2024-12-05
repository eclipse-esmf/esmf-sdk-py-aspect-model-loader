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

from typing import List

from esmf_aspect_meta_model_python.base.characteristics.enumeration import Enumeration
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEnumeration(DefaultCharacteristic, Enumeration):
    """Default Enumeration class."""

    LIST_ATTR_NAMES = DefaultCharacteristic.LIST_ATTR_NAMES + ["values"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: DataType,
        values: List,
    ):
        super().__init__(meta_model_base_attributes, data_type)
        self._values = values

    @property
    def values(self) -> List:
        """Values."""
        return self._values
