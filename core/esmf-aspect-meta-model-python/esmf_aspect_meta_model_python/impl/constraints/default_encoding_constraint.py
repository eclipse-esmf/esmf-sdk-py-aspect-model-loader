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

from esmf_aspect_meta_model_python.base.contraints.encoding_constraint import EncodingConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEncodingConstraint(DefaultConstraint, EncodingConstraint):
    """Default Encoding Constraint class."""

    SCALAR_ATTR_NAMES = DefaultConstraint.SCALAR_ATTR_NAMES + ["value"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, value: str):
        super().__init__(meta_model_base_attributes)
        self._value = value

    @property
    def value(self) -> str:
        """Value."""
        return self._value
