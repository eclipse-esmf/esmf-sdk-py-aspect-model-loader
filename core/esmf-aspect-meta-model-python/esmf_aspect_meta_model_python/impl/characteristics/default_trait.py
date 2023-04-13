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

from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.contraints.constraint import Constraint
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic


class DefaultTrait(DefaultCharacteristic, Trait):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, base_characteristic: Characteristic, constraints: List[Constraint]):
        if base_characteristic is None:
            raise AttributeError(f"No base characteristic given for the trait {self.urn}")

        if not constraints:
            raise AttributeError(f"No constraints given for the trait {self.urn}")

        super().__init__(meta_model_base_attributes, base_characteristic.data_type)

        self._base_characteristic: Characteristic = base_characteristic
        self._constraints: List[Constraint] = constraints

    @property
    def base_characteristic(self) -> Characteristic:
        return self._base_characteristic

    @property
    def constraints(self) -> List[Constraint]:
        return self._constraints
