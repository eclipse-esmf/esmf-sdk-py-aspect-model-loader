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


class StructuredValue(Characteristic, ABC):
    """Interface for a structured value characteristic.

    Describes a property with a string-like data type where the value has a specific defined structure that can be
    deconstructed with a regular expression.
    """

    @property
    @abstractmethod
    def deconstruction_rule(self) -> Optional[str]:
        """Returns the deconstruction rule for the structured value.

        Returns:
            Optional[str]: The deconstruction rule as a string, or None if not set.
        """

    @property
    @abstractmethod
    def elements(self) -> List:
        """Returns the elements that make up the structured value.

        Returns:
            List: The list of elements that make up the structured value.
        """
