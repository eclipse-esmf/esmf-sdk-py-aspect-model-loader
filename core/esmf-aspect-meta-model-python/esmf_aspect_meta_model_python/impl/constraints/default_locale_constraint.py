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

from esmf_aspect_meta_model_python.base.contraints.locale_constraint import LocaleConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultLocaleConstraint(DefaultConstraint, LocaleConstraint):
    """Default Locale Constraint class."""

    SCALAR_ATTR_NAMES = DefaultConstraint.SCALAR_ATTR_NAMES + ["locale_code"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, locale_code: str):
        super().__init__(meta_model_base_attributes)
        self._locale_code = locale_code

    @property
    def locale_code(self) -> str:
        """locale code."""
        return self._locale_code
