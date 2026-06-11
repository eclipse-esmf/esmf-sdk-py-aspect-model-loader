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

from esmf_aspect_meta_model_python.base.constraints.locale_constraint import LocaleConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultLocaleConstraint(DefaultConstraint, LocaleConstraint):
    """Default implementation of a locale constraint.

    Represents a locale constraint with a required locale code.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultConstraint.SCALAR_ATTR_NAMES + ["locale_code"]
    REQUIRED_ATTRS: List[str] = DefaultConstraint.REQUIRED_ATTRS + ["locale_code"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, locale_code: Optional[str]):
        """Initializes the DefaultLocaleConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            locale_code (Optional[str]): The locale code for the constraint.
        """
        super().__init__(meta_model_base_attributes)

        self._locale_code = locale_code

    @property
    def locale_code(self) -> Optional[str]:
        """Returns the locale code for the constraint.

        Returns:
            Optional[str]: The locale code, or None if not set.
        """
        return self._locale_code

    @locale_code.setter
    def locale_code(self, locale_code: str) -> None:
        """Sets the locale code for the constraint.

        Args:
            locale_code (str): The locale code to set.

        Raises:
            ValueError: If the provided locale_code is None or empty.
        """
        if not locale_code:
            raise ValueError("Locale code cannot be None.")

        self._locale_code = locale_code
