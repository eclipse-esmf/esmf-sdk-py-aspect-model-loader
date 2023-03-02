#  Copyright (c) 2022 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from typing import Optional, Any

from esmf_aspect_meta_model_python.base.bound_definition import BoundDefinition
from esmf_aspect_meta_model_python.base.contraints.range_constraint import RangeConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint


class DefaultRangeConstraint(DefaultConstraint, RangeConstraint):
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
    def min_value(self) -> Optional[Any]:
        return self._min_value

    @property
    def max_value(self) -> Optional[Any]:
        return self._max_value

    @property
    def lower_bound_definition(self) -> Optional[BoundDefinition]:
        return self._lower_bound_definition

    @property
    def upper_bound_definition(self) -> Optional[BoundDefinition]:
        return self._upper_bound_definition
