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

from typing import Tuple

from esmf_aspect_meta_model_python.base.constraints.encoding_constraint import EncodingConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEncodingConstraint(DefaultConstraint, EncodingConstraint):
    """Default implementation of an encoding constraint.

    Represents an encoding constraint with a required value.
    """

    SCALAR_ATTR_NAMES: Tuple[str, ...] = DefaultConstraint.SCALAR_ATTR_NAMES + ("value",)
    REQUIRED_ATTRS: Tuple[str, ...] = DefaultConstraint.REQUIRED_ATTRS + ("value",)

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, value: str):
        """Initializes the DefaultEncodingConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            value (str): The value for the encoding constraint.
        """
        super().__init__(meta_model_base_attributes)

        self._value = value

    @property
    def value(self) -> str:
        """Returns the value for the encoding constraint.

        Returns:
            str: The value, or None if not set.
        """
        return self._value
