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

from typing import Any, Optional

from esmf_aspect_meta_model_python.base.bound_definition import BoundDefinition
from esmf_aspect_meta_model_python.base.constraints.range_constraint import RangeConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultRangeConstraint(DefaultConstraint, RangeConstraint):
    """Default Range Constraint class."""

    SCALAR_ATTR_NAMES = DefaultConstraint.SCALAR_ATTR_NAMES + [
        "min_value",
        "max_value",
        "lower_bound_definition",
        "upper_bound_definition",
    ]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        min_value: Optional[Any],
        max_value: Optional[Any],
        lower_bound_definition: Optional[BoundDefinition],
        upper_bound_definition: Optional[BoundDefinition],
    ):
        super().__init__(meta_model_base_attributes)

        self._min_value = min_value
        self._max_value = max_value
        self._lower_bound_definition = lower_bound_definition
        self._upper_bound_definition = upper_bound_definition

    @property
    def min_value(self) -> Any:
        """Min value."""
        return self._min_value
    
    @min_value.setter
    def min_value(self, min_value: Any) -> None:
        """Min value setter."""
        if min_value is None:
            raise ValueError("Min value cannot be None.")
        
        self._min_value = min_value

    @property
    def max_value(self) -> Optional[Any]:
        """Max value."""
        return self._max_value
    
    @max_value.setter
    def max_value(self, max_value: Any) -> None:
        """Max value setter."""
        if max_value is None:
            raise ValueError("Max value cannot be None.")
        
        self._max_value = max_value

    @property
    def lower_bound_definition(self) -> Optional[BoundDefinition]:
        """Lower bound definition."""
        return self._lower_bound_definition

    @property
    def upper_bound_definition(self) -> Optional[BoundDefinition]:
        """Upper bound definition."""
        return self._upper_bound_definition
