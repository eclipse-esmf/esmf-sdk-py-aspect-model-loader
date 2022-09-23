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

from sds_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from sds_aspect_meta_model_python.base.data_types.data_type import DataType
from sds_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from sds_aspect_meta_model_python.impl.base_impl import BaseImpl
from sds_aspect_meta_model_python.base.data_types.complex_type import ComplexType


class DefaultCharacteristic(BaseImpl, Characteristic):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, data_type: DataType):
        super().__init__(meta_model_base_attributes)
        self._data_type = data_type

        if isinstance(self._data_type, ComplexType):
            self._data_type.append_parent_element(self)

    @property
    def data_type(self) -> DataType:
        return self._data_type
