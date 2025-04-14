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

from typing import Any

from esmf_aspect_meta_model_python.base.value import Value
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultValue(BaseImpl, Value):
    """Default value class."""

    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + ["value"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        value: Any,
    ):
        super().__init__(meta_model_base_attributes)
        self._value = value

    @property
    def value(self) -> Any:
        """Value."""
        return self._value
