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

from typing import Optional

from esmf_aspect_meta_model_python.base.constraints.fixed_point_constraint import FixedPointConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultFixedPointConstraint(DefaultConstraint, FixedPointConstraint):
    """Default Fixed Point Constraint class."""

    SCALAR_ATTR_NAMES = DefaultConstraint.SCALAR_ATTR_NAMES + ["scale", "integer"]
    REQUIRED_ATTRS = DefaultConstraint.REQUIRED_ATTRS + ["scale", "integer"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        scale: Optional[int],
        integer: Optional[int],
    ):
        super().__init__(meta_model_base_attributes)
        self._scale = scale
        self._integer = integer

    @property
    def scale(self) -> Optional[int]:
        """Scale."""
        return self._scale

    @scale.setter
    def scale(self, scale: int) -> None:
        """Scale setter."""
        if not scale:
            raise ValueError("Scale cannot be None.")
        
        self._scale = scale

    @property
    def integer(self) -> Optional[int]:
        """Integer."""
        return self._integer

    @integer.setter
    def integer(self, integer: int) -> None:
        """Integer setter."""
        if not integer:
            raise ValueError("Integer cannot be None.")
        
        self._integer = integer
