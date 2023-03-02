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

from typing import Optional

from esmf_aspect_meta_model_python.base.contraints.length_constraint import LengthConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint


class DefaultLengthConstraint(DefaultConstraint, LengthConstraint):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, min_value: Optional[int], max_value: Optional[int]):
        super().__init__(meta_model_base_attributes)
        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self) -> Optional[int]:
        return self._min_value

    @property
    def max_value(self) -> Optional[int]:
        return self._max_value
