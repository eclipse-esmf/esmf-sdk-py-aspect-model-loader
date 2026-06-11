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

from esmf_aspect_meta_model_python.base.constraints.encoding_constraint import EncodingConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEncodingConstraint(DefaultConstraint, EncodingConstraint):
    """Default implementation of an encoding constraint.

    Represents an encoding constraint with a required value.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultConstraint.SCALAR_ATTR_NAMES + ["value"]
    REQUIRED_ATTRS: List[str] = DefaultConstraint.REQUIRED_ATTRS + ["value"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, value: Optional[str]):
        """Initializes the DefaultEncodingConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            value (Optional[str]): The value for the encoding constraint.
        """
        super().__init__(meta_model_base_attributes)

        self._value = value

    @property
    def value(self) -> Optional[str]:
        """Returns the value for the encoding constraint.

        Returns:
            Optional[str]: The value, or None if not set.
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """Sets the value for the encoding constraint.

        Args:
            value (str): The value to set.

        Raises:
            ValueError: If the provided value is None or empty.
        """
        if not value:
            raise ValueError("Value cannot be None.")

        self._value = value
