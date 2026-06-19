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


class EncodingConstraint(Constraint, ABC):
    """Encoding Constraint interface class.

    Restricts the encoding of a Property (e.g., samm:UTF-8, samm:US:ASCII).
    """

    @property
    @abstractmethod
    def value(self) -> Optional[str]:
        """Returns the encoding value for the constraint.

        Returns:
            Optional[str]: The encoding value as a string, or None if not set.
        """
