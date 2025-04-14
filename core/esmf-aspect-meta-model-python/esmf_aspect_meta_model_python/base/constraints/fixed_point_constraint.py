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

from esmf_aspect_meta_model_python.base.constraints.constraint import Constraint


class FixedPointConstraint(Constraint, ABC):
    """Fixed Point Constraint interface class.

    Defines the scaling factor as well as the amount of integral numbers for a fixed point number.
    The constraint may only be used in conjunction with Characteristics which use the xsd:decimal data type.
    """

    @property
    @abstractmethod
    def scale(self) -> int:
        """Scale."""

    @property
    @abstractmethod
    def integer(self) -> int:
        """Integer."""
