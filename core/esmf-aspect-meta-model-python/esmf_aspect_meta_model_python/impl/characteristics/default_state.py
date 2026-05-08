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

from typing import Any, List, Optional

from esmf_aspect_meta_model_python.base.characteristics.state import State
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.characteristics.default_enumeration import DefaultEnumeration
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultState(DefaultEnumeration, State):
    """Default State class."""

    SCALAR_ATTR_NAMES = DefaultEnumeration.SCALAR_ATTR_NAMES + ["default_value"]
    # TODO: Check if default_value should be added to REQUIRED_ATTRS
    # Can the dafault_value be None? If not, it should be added to REQUIRED_ATTRS and added a check with raising exception if empty
    # REQUIRED_ATTRS = DefaultEnumeration.REQUIRED_ATTRS + ["default_value"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: Optional[DataType],
        values: Optional[List],
        default_value: Any,
    ):
        super().__init__(meta_model_base_attributes, data_type, values)
        self._default_value = default_value

    @property
    def default_value(self):
        """Default value."""
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        """Default value setter."""
        self._default_value = value
