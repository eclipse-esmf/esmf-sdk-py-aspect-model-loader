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

from esmf_aspect_meta_model_python.base.constraints.length_constraint import LengthConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultLengthConstraint(DefaultConstraint, LengthConstraint):
    """Default implementation of a length constraint.

    Represents a length constraint with optional minimum and maximum values.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultConstraint.SCALAR_ATTR_NAMES + ["min_value", "max_value"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        min_value: Optional[int],
        max_value: Optional[int],
    ):
        """Initializes the DefaultLengthConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            min_value (Optional[int]): The minimum value for the constraint.
            max_value (Optional[int]): The maximum value for the constraint.
        """
        super().__init__(meta_model_base_attributes)

        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self) -> Optional[int]:
        """Returns the minimum value for the length constraint.

        Returns:
            Optional[int]: The minimum value, or None if not set.
        """
        return self._min_value

    @min_value.setter
    def min_value(self, min_value: int) -> None:
        """Sets the minimum value for the length constraint.

        Args:
            min_value (int): The minimum value to set.

        Raises:
            ValueError: If the provided min_value is None or zero.
        """
        if not min_value:
            raise ValueError("Min value cannot be None.")

        self._min_value = min_value

    @property
    def max_value(self) -> Optional[int]:
        """Returns the maximum value for the length constraint.

        Returns:
            Optional[int]: The maximum value, or None if not set.
        """
        return self._max_value

    @max_value.setter
    def max_value(self, max_value: int) -> None:
        """Sets the maximum value for the length constraint.

        Args:
            max_value (int): The maximum value to set.

        Raises:
            ValueError: If the provided max_value is None or zero.
        """
        if not max_value:
            raise ValueError("Max value cannot be None.")

        self._max_value = max_value
