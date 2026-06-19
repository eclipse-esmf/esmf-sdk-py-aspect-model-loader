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

from typing import List, Tuple

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.constraints.constraint import Constraint
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultTrait(DefaultCharacteristic, Trait):
    """Default implementation of a trait characteristic.

    Represents a trait with a base characteristic and a list of constraints.
    """

    SCALAR_ATTR_NAMES: Tuple[str, ...] = DefaultCharacteristic.SCALAR_ATTR_NAMES + ("base_characteristic",)
    LIST_ATTR_NAMES: Tuple[str, ...] = DefaultCharacteristic.LIST_ATTR_NAMES + ("constraints",)
    REQUIRED_ATTRS: Tuple[str, ...] = DefaultCharacteristic.REQUIRED_ATTRS + ("base_characteristic", "constraints")

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        base_characteristic: Characteristic,
        constraints: List[Constraint],
    ):
        """Initializes the DefaultTrait.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            base_characteristic (Characteristic): The base characteristic for the trait.
            constraints (List[Constraint]): The list of constraints for the trait.
        """
        super().__init__(meta_model_base_attributes, base_characteristic.data_type if base_characteristic else None)

        self._trait_urn = meta_model_base_attributes.urn
        self._base_characteristic: Characteristic = base_characteristic
        self._constraints: List[Constraint] = constraints

    @property
    def base_characteristic(self) -> Characteristic:
        """Returns the base characteristic for the trait.

        Returns:
            Characteristic: The base characteristic, or None if not set.
        """
        return self._base_characteristic

    @property
    def constraints(self) -> List[Constraint]:
        """Returns the list of constraints for the trait.

        Returns:
            List[Constraint]: The list of constraints.
        """
        return self._constraints
