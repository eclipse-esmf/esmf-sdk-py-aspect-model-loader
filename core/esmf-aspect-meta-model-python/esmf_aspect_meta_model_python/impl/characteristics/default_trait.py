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
from esmf_aspect_meta_model_python.base.characteristics.trait import Trait
from esmf_aspect_meta_model_python.base.constraints.constraint import Constraint
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultTrait(DefaultCharacteristic, Trait):
    """Default implementation of a trait characteristic.

    Represents a trait with a base characteristic and a list of constraints.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultCharacteristic.SCALAR_ATTR_NAMES + ["base_characteristic"]
    LIST_ATTR_NAMES: List[str] = DefaultCharacteristic.LIST_ATTR_NAMES + ["constraints"]
    REQUIRED_ATTRS = DefaultCharacteristic.REQUIRED_ATTRS + ["base_characteristic", "constraints"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        base_characteristic: Optional[Characteristic],
        constraints: List[Constraint],
    ):
        """Initializes the DefaultTrait.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            base_characteristic (Optional[Characteristic]): The base characteristic for the trait.
            constraints (List[Constraint]): The list of constraints for the trait.
        """
        super().__init__(meta_model_base_attributes, base_characteristic.data_type if base_characteristic else None)

        self._trait_urn = meta_model_base_attributes.urn
        self._base_characteristic: Optional[Characteristic] = base_characteristic
        self._constraints: List[Constraint] = constraints

    @property
    def base_characteristic(self) -> Optional[Characteristic]:
        """Returns the base characteristic for the trait.

        Returns:
            Optional[Characteristic]: The base characteristic, or None if not set.
        """
        return self._base_characteristic

    @base_characteristic.setter
    def base_characteristic(self, base_characteristic: Characteristic) -> None:
        """Sets the base characteristic for the trait.

        Args:
            base_characteristic (Characteristic): The base characteristic to set.

        Raises:
            AttributeError: If the provided base_characteristic is None.
        """
        if not base_characteristic:
            raise AttributeError(f"No base characteristic given for the trait {self._trait_urn}")

        self._base_characteristic = base_characteristic

    @property
    def constraints(self) -> List[Constraint]:
        """Returns the list of constraints for the trait.

        Returns:
            List[Constraint]: The list of constraints.
        """
        return self._constraints

    @constraints.setter
    def constraints(self, constraints: List[Constraint]) -> None:
        """Sets the list of constraints for the trait.

        Args:
            constraints (List[Constraint]): The list of constraints to set.

        Raises:
            AttributeError: If the provided constraints list is None or empty.
        """
        if not constraints:
            raise AttributeError(f"No constraints given for the trait {self._trait_urn}")

        self._constraints = constraints
