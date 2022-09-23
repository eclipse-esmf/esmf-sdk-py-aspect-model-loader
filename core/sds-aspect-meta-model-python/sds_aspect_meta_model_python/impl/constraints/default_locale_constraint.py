#  Copyright (c) 2022 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from sds_aspect_meta_model_python.base.contraints.locale_constraint import LocaleConstraint
from sds_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from sds_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint


class DefaultLocaleConstraint(DefaultConstraint, LocaleConstraint):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, locale_code: str):
        super().__init__(meta_model_base_attributes)
        self._locale_code = locale_code

    @property
    def locale_code(self) -> str:
        return self._locale_code
