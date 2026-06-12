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

from esmf_aspect_meta_model_python.base.constraints.locale_constraint import LocaleConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultLocaleConstraint(DefaultConstraint, LocaleConstraint):
    """Default implementation of a locale constraint.

    Represents a locale constraint with a required locale code.
    """

    SCALAR_ATTR_NAMES: Tuple[str, ...] = DefaultConstraint.SCALAR_ATTR_NAMES + ("locale_code",)
    REQUIRED_ATTRS: Tuple[str, ...] = DefaultConstraint.REQUIRED_ATTRS + ("locale_code",)

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, locale_code: str):
        """Initializes the DefaultLocaleConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            locale_code (str): The locale code for the constraint.
        """
        super().__init__(meta_model_base_attributes)

        self._locale_code = locale_code

    @property
    def locale_code(self) -> str:
        """Returns the locale code for the constraint.

        Returns:
            str: The locale code, or None if not set.
        """
        return self._locale_code
