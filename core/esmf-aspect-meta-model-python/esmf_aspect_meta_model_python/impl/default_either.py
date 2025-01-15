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

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.either import Either
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEither(BaseImpl, Either):
    """Default Either class."""

    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + ["left", "right"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        left: Characteristic,
        right: Characteristic,
    ):
        super().__init__(meta_model_base_attributes)

        left.append_parent_element(self)
        self._left = left

        right.append_parent_element(self)
        self._right = right

    @property
    def left(self) -> Characteristic:
        """Left."""
        return self._left

    @property
    def right(self) -> Characteristic:
        """Right."""
        return self._right
