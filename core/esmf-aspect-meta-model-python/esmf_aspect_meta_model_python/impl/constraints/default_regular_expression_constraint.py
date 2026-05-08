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

from esmf_aspect_meta_model_python.base.constraints.regular_expression_constraint import RegularExpressionConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultRegularExpressionConstraint(DefaultConstraint, RegularExpressionConstraint):
    """Default Regular Expression Constraint."""

    SCALAR_ATTR_NAMES = DefaultConstraint.SCALAR_ATTR_NAMES + ["value"]
    REQUIRED_ATTRS = DefaultConstraint.REQUIRED_ATTRS + ["value"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, value: Optional[str]):
        super().__init__(meta_model_base_attributes)

        self._value = value

    @property
    def value(self) -> Optional[str]:
        """Value."""
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """Value setter."""
        if not value:
            raise ValueError("Value cannot be None.")
        
        self._value = value
