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

from abc import ABC, abstractmethod
from typing import List, Optional

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic

from ..constraints import constraint


class Trait(Characteristic, ABC):
    """Trait interface class.

    Describes a property where the value is restricted by one or more constraints.
    A Trait has one base characteristic which describes the actual value and a number of constraints which restrict
    this value.
    """

    @property
    @abstractmethod
    def base_characteristic(self) -> Optional[Characteristic]:
        """Returns the base characteristic for the trait.

        Returns:
            Optional[Characteristic]: The base characteristic, or None if not set.
        """

    @property
    @abstractmethod
    def constraints(self) -> List[constraint.Constraint]:
        """Returns the constraints for the trait.

        Returns:
            List[Constraint]: The list of constraints that restrict the trait's value.
        """
