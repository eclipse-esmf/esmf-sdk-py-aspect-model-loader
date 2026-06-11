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
from typing import Optional

from esmf_aspect_meta_model_python.base.constraints.constraint import Constraint


class FixedPointConstraint(Constraint, ABC):
    """Fixed Point Constraint interface class.

    Defines the scaling factor and the number of integral digits for a fixed point number.
    The constraint may only be used with Characteristics that use the xsd:decimal data type.
    """

    @property
    @abstractmethod
    def scale(self) -> Optional[int]:
        """Returns the scaling factor for the fixed point constraint.

        Returns:
            Optional[int]: The scaling factor, or None if not set.
        """

    @property
    @abstractmethod
    def integer(self) -> Optional[int]:
        """Returns the number of integral digits for the fixed point constraint.

        Returns:
            Optional[int]: The number of integral digits, or None if not set.
        """
