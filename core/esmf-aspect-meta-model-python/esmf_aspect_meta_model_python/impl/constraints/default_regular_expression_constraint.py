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

from esmf_aspect_meta_model_python.base.constraints.regular_expression_constraint import RegularExpressionConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultRegularExpressionConstraint(DefaultConstraint, RegularExpressionConstraint):
    """Default implementation of a regular expression constraint.

    Represents a regular expression constraint with a required value.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultConstraint.SCALAR_ATTR_NAMES + ["value"]
    REQUIRED_ATTRS: List[str] = DefaultConstraint.REQUIRED_ATTRS + ["value"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, value: Optional[str]):
        """Initializes the DefaultRegularExpressionConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            value (Optional[str]): The regular expression value for the constraint.
        """
        super().__init__(meta_model_base_attributes)

        self._value = value

    @property
    def value(self) -> Optional[str]:
        """Returns the regular expression value for the constraint.

        Returns:
            Optional[str]: The regular expression value, or None if not set.
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """Sets the regular expression value for the constraint.

        Args:
            value (str): The regular expression value to set.

        Raises:
            ValueError: If the provided value is None or empty.
        """
        if not value:
            raise ValueError("Value cannot be None.")

        self._value = value
