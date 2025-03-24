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
from esmf_aspect_meta_model_python.base.data_types.complex_type import ComplexType
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultCharacteristic(BaseImpl, Characteristic):
    """Default Characteristic class."""

    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + ["data_type"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, data_type: Optional[DataType]):
        if data_type is None:
            raise ValueError("Attribute 'data_type' is required for Characteristic class.")

        super().__init__(meta_model_base_attributes)

        self._data_type = data_type

        if isinstance(self._data_type, ComplexType):
            self._data_type.append_parent_element(self)

    @property
    def data_type(self) -> DataType:
        """Data type."""
        return self._data_type
