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

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.either import Either
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEither(BaseImpl, Either):
    """Default Either class."""

    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + ["left", "right"]
    REQUIRED_ATTRS = BaseImpl.REQUIRED_ATTRS + ["left", "right"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        left: Optional[Characteristic],
        right: Optional[Characteristic],
    ):
        super().__init__(meta_model_base_attributes)

        self._left = left
        if self._left:
            self._left.append_parent_element(self)
        
        self._right = right
        if self._right:
            self._right.append_parent_element(self)
        

    @property
    def left(self) -> Characteristic:
        """Left."""
        return self._left

    @left.setter
    def left(self, left: Characteristic) -> None:
        """Left."""
        self._left = left
        if self._left:
            self._left.append_parent_element(self)
        
    @property
    def right(self) -> Characteristic:
        """Right."""
        return self._right

    @right.setter
    def right(self, right: Characteristic) -> None:
        """Right."""
        self._right = right
        if self._right:
            self._right.append_parent_element(self)
