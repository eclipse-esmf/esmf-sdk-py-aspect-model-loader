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

from esmf_aspect_meta_model_python.base.characteristics.quantifiable.quantifiable import Quantifiable
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.base.unit import Unit
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultQuantifiable(DefaultCharacteristic, Quantifiable):
    """Default Quantifiable class."""

    LIST_ATTR_NAMES = DefaultCharacteristic.LIST_ATTR_NAMES + ["unit"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: DataType,
        unit: Optional[Unit],
    ):
        super().__init__(meta_model_base_attributes, data_type)
        self._unit = unit
        if self.unit is not None:
            self.unit.append_parent_element(self)

    @property
    def unit(self) -> Optional[Unit]:
        """Unit."""
        return self._unit
