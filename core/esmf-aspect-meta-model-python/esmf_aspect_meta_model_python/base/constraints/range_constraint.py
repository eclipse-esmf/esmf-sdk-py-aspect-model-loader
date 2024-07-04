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
from typing import Any, Optional

from esmf_aspect_meta_model_python.base.bound_definition import BoundDefinition
from esmf_aspect_meta_model_python.base.constraints.constraint import Constraint


class RangeConstraint(Constraint, ABC):
    """Range Constraint interface class.

    Restricts the value range of a Property.
    At least one of samm-c:maxValue or samm-c:minValue must be present in a Range Constraint.
    Additionally, the Bound Definition can specify whether the upper and lower value are included in the range.
    """

    @property
    @abstractmethod
    def min_value(self) -> Optional[Any]:
        """Min value."""

    @property
    @abstractmethod
    def max_value(self) -> Optional[Any]:
        """Max value."""

    @property
    @abstractmethod
    def lower_bound_definition(self) -> Optional[BoundDefinition]:
        """Lower bound definition."""

    @property
    @abstractmethod
    def upper_bound_definition(self) -> Optional[BoundDefinition]:
        """Upper bound definition."""
