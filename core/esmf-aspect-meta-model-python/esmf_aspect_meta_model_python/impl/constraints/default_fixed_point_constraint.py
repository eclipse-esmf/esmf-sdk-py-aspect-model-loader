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

from typing import List, Optional

from esmf_aspect_meta_model_python.base.constraints.fixed_point_constraint import FixedPointConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultFixedPointConstraint(DefaultConstraint, FixedPointConstraint):
    """Default implementation of a fixed point constraint.

    Represents a fixed point constraint with required scale and integer values.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultConstraint.SCALAR_ATTR_NAMES + ["scale", "integer"]
    REQUIRED_ATTRS: List[str] = DefaultConstraint.REQUIRED_ATTRS + ["scale", "integer"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        scale: Optional[int],
        integer: Optional[int],
    ):
        """Initializes the DefaultFixedPointConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            scale (Optional[int]): The scale value for the constraint.
            integer (Optional[int]): The integer value for the constraint.
        """
        super().__init__(meta_model_base_attributes)
        self._scale = scale
        self._integer = integer

    @property
    def scale(self) -> Optional[int]:
        """Returns the scale value for the fixed point constraint.

        Returns:
            Optional[int]: The scale value, or None if not set.
        """
        return self._scale

    @scale.setter
    def scale(self, scale: int) -> None:
        """Sets the scale value for the fixed point constraint.

        Args:
            scale (int): The scale value to set.

        Raises:
            ValueError: If the provided scale is None or zero.
        """
        if not scale:
            raise ValueError("Scale cannot be None.")

        self._scale = scale

    @property
    def integer(self) -> Optional[int]:
        """Returns the integer value for the fixed point constraint.

        Returns:
            Optional[int]: The integer value, or None if not set.
        """
        return self._integer

    @integer.setter
    def integer(self, integer: int) -> None:
        """Sets the integer value for the fixed point constraint.

        Args:
            integer (int): The integer value to set.

        Raises:
            ValueError: If the provided integer is None or zero.
        """
        if not integer:
            raise ValueError("Integer cannot be None.")

        self._integer = integer
