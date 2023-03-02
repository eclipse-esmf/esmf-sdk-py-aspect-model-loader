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

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.characteristics.either import Either
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic


class DefaultEither(DefaultCharacteristic, Either):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, data_type: DataType, left: Characteristic, right: Characteristic):
        super().__init__(meta_model_base_attributes, data_type)

        left.append_parent_element(self)
        self._left = left

        right.append_parent_element(self)
        self._right = right

    @property
    def left(self) -> Characteristic:
        return self._left

    @property
    def right(self) -> Characteristic:
        return self._right
